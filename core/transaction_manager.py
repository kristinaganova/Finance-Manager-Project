import pandas as pd
from decimal import Decimal
from datetime import datetime, timedelta
import sqlite3
from utils.initialize_database import DATABASE_PATH
import seaborn as sns
from sklearn.cluster import KMeans
import matplotlib.pyplot as  plt

class TransactionManager:
    def __init__(self, conn, user, account_manager, currency_converter=None):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.user = user
        self.account_manager = account_manager  
        self.currency_converter = currency_converter
        self.transactions = self.load_transactions()

    def load_transactions(self):
        self.cursor.execute('''
            SELECT t.id, t.date, t.category, t.amount, t.type, t.currency, pm.method_name
            FROM transactions t
            JOIN payment_methods pm ON t.payment_method_id = pm.id
            WHERE t.user_id = ?
        ''', (self.user.user_id,))
        transactions = self.cursor.fetchall()

        transactions_df = pd.DataFrame(transactions, columns=['ID', 'Date', 'Category', 'Amount', 'Type', 'Currency', 'Payment Method'])
        return transactions_df

    def remove_transaction(self, transaction_id):
        if self.user is None:
            raise ValueError("No user logged in")

        self.cursor.execute('''
            SELECT amount, type, payment_method_id
            FROM transactions
            WHERE id = ? AND user_id = ?
        ''', (transaction_id, self.user.user_id))
        transaction = self.cursor.fetchone()

        if not transaction:
            raise ValueError("Transaction not found.")

        amount, transaction_type, payment_method_id = transaction

        self.cursor.execute('''
            SELECT method_name
            FROM payment_methods
            WHERE id = ? AND user_id = ?
        ''', (payment_method_id, self.user.user_id))
        payment_method_name = self.cursor.fetchone()[0]

        self.account_manager.update_balance(payment_method_name, Decimal(amount), transaction_type)

        self.cursor.execute('''
            DELETE FROM transactions
            WHERE id = ? AND user_id = ?
        ''', (transaction_id, self.user.user_id))
        self.conn.commit()

        self.transactions = self.load_transactions()

    def add_transaction(self, date, category, amount, transaction_type, payment_method, currency='BGN'):
        if self.user is None:
            raise ValueError("No user logged in")
        
        amount_in_BGN = self.currency_converter.convert_currency(amount, currency, 'BGN') if self.currency_converter else amount
        
        self._store_transaction_in_db(date, category, amount_in_BGN, transaction_type, payment_method, currency)
        
        if transaction_type == 'Income':
            self.account_manager.update_balance(payment_method, amount_in_BGN, 'Income')
        elif transaction_type == 'Expense':
            self.account_manager.update_balance(payment_method, amount_in_BGN, 'Expense')
        
        self.transactions = self.load_transactions()


    def get_transactions(self, target_currency='BGN'):
        transactions = self._retrieve_transactions_from_db()
        transactions_df = pd.DataFrame(transactions, columns=['ID', 'Date', 'Category', 'Amount', 'Type', 'Currency', 'Payment Method'])

        if target_currency != 'BGN' and self.currency_converter:
            transactions_df['Amount'] = transactions_df.apply(
                lambda row: self.currency_converter.convert_currency(Decimal(row['Amount']), 'BGN', target_currency), axis=1)
            transactions_df['Currency'] = target_currency

        return transactions_df

    def calculate_statistics(self, target_currency='BGN'):
        transactions = self.get_transactions(target_currency)
        expenses = transactions[transactions['Type'] == 'Expense']['Amount'].apply(Decimal)
        income = transactions[transactions['Type'] == 'Income']['Amount'].apply(Decimal)

        stats = {
            'Mean Expense': round(sum(expenses) / len(expenses), 2) if len(expenses) > 0 else Decimal(0),
            'Median Expense': round(sorted(expenses)[len(expenses) // 2], 2) if len(expenses) > 0 else Decimal(0),
            'Std Dev Expense': round((sum((x - (sum(expenses) / len(expenses))) ** 2 for x in expenses) / len(expenses)).sqrt(), 2) if len(expenses) > 0 else Decimal(0),
            'Mean Income': round(sum(income) / len(income), 2) if len(income) > 0 else Decimal(0),
            'Median Income': round(sorted(income)[len(income) // 2], 2) if len(income) > 0 else Decimal(0),
            'Std Dev Income': round((sum((x - (sum(income) / len(income))) ** 2 for x in income) / len(income)).sqrt(), 2) if len(income) > 0 else Decimal(0),
        }
        return stats

    def calculate_correlations(self, target_currency='BGN'):
        transactions = self.get_transactions(target_currency)
        expenses = transactions[transactions['Type'] == 'Expense']
        expenses_by_category = expenses.pivot_table(values='Amount', index='Date', columns='Category', aggfunc='sum', fill_value=Decimal(0))
        correlations = expenses_by_category.corr()
        return correlations

    def forecast(self, days_ahead=30, target_currency='BGN'):
        transactions = self.get_transactions(target_currency)
        
        # Convert the Date column to datetime if it's not already
        transactions['Date'] = pd.to_datetime(transactions['Date'], errors='coerce')

        # Drop any rows where the Date conversion failed
        transactions = transactions.dropna(subset=['Date'])

        transactions['Date_ordinal'] = transactions['Date'].apply(lambda x: x.toordinal())

        expenses = transactions[transactions['Type'] == 'Expense']
        income = transactions[transactions['Type'] == 'Income']

        def linear_regression(x, y):
            n = len(x)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum(x_i * y_i for x_i, y_i in zip(x, y))
            sum_x_squared = sum(x_i ** 2 for x_i in x)

            denominator = (n * sum_x_squared - sum_x ** 2)
            if denominator == 0:
                return 0, sum_y / n if n != 0 else 0

            a = (n * sum_xy - sum_x * sum_y) / denominator
            b = (sum_y - a * sum_x) / n
            return a, b

        future_expenses = [Decimal(0)] * days_ahead
        future_income = [Decimal(0)] * days_ahead

        if len(expenses) > 0:
            x_exp = expenses['Date_ordinal'].tolist()
            y_exp = expenses['Amount'].astype(float).tolist()
            a_exp, b_exp = linear_regression(x_exp, y_exp)

            future_expenses = [Decimal(a_exp * (datetime.now() + timedelta(days=i)).toordinal() + b_exp) for i in range(1, days_ahead + 1)]

        if len(income) > 0:
            x_inc = income['Date_ordinal'].tolist()
            y_inc = income['Amount'].astype(float).tolist()
            a_inc, b_inc = linear_regression(x_inc, y_inc)

            future_income = [Decimal(a_inc * (datetime.now() + timedelta(days=i)).toordinal() + b_inc) for i in range(1, days_ahead + 1)]

        return future_expenses, future_income

    
    def get_total_income_and_expense(self):
        transactions = self.get_transactions() 
        income_total = transactions[transactions['Type'] == 'Income']['Amount'].sum()
        expense_total = transactions[transactions['Type'] == 'Expense']['Amount'].sum()
        return income_total, expense_total

    def _store_transaction_in_db(self, date, category, amount, transaction_type, payment_method, currency):
        amount_in_BGN = self.currency_converter.convert_currency(amount, currency, 'BGN') if self.currency_converter and currency != 'BGN' else amount
        if self.user is None:
            raise ValueError("No user logged in")
        
        self.cursor.execute('''
            INSERT INTO transactions (user_id, date, category, amount, type, payment_method_id, currency)
            VALUES (?, ?, ?, ?, ?, (SELECT id FROM payment_methods WHERE user_id = ? AND method_name = ?), ?)
        ''', (self.user.user_id, date, category, float(amount_in_BGN), transaction_type, self.user.user_id, payment_method, currency))
        
        self.conn.commit()

    def _retrieve_transactions_from_db(self):
        if self.user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            SELECT t.id, t.date, t.category, t.amount, t.type, t.currency, pm.method_name
            FROM transactions t
            JOIN payment_methods pm ON t.payment_method_id = pm.id
            WHERE t.user_id = ?
        ''', (self.user.user_id,))
        transactions = self.cursor.fetchall()
        return transactions
