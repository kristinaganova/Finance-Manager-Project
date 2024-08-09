import sqlite3
from decimal import Decimal
from currency_converter import CurrencyConverter
from user import User
from account_manager import AccountManager
from transaction_manager import TransactionManager
from goal_manager import GoalManager
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

class FinanceManager:
    def __init__(self):
        self.conn = sqlite3.connect('finance_manager.db')
        self.cursor = self.conn.cursor()
        self.currency_converter = CurrencyConverter()
        self.account_manager = AccountManager()
        self.transaction_manager = TransactionManager(self.currency_converter, self.account_manager)
        self.goal_manager = GoalManager()
        self.current_user = None

    def set_user(self, user):
        self.current_user = user

    def add_payment_method(self, method_name, method_type, initial_balance=Decimal('0.00')):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            INSERT INTO payment_methods (user_id, method_name, method_type, balance)
            VALUES (?, ?, ?, ?)
        ''', (self.current_user.user_id, method_name, method_type, float(initial_balance)))
        self.conn.commit()
        self.account_manager.add_payment_method(method_name, method_type, initial_balance)
        
        # Add initial balance as a transaction
        #self.add_transaction(datetime.now().date(), f"Initial Balance: {method_name}", initial_balance, "Income", method_name, "BGN")

    def add_transaction(self, date, category, amount, transaction_type, payment_method_name, currency='BGN'):
        if self.current_user is None:
            raise ValueError("No user logged in")
        
        # Find the payment method ID
        self.cursor.execute('''
            SELECT id FROM payment_methods
            WHERE user_id = ? AND method_name = ?
        ''', (self.current_user.user_id, payment_method_name))
        payment_method_id = self.cursor.fetchone()
        
        if not payment_method_id:
            raise ValueError("Payment method not found")
        
        payment_method_id = payment_method_id[0]

        amount_in_BGN = self.currency_converter.convert_currency(amount, currency, 'BGN')
        self.cursor.execute('''
            INSERT INTO transactions (user_id, date, category, amount, type, payment_method_id, currency)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.current_user.user_id, date, category, float(amount_in_BGN), transaction_type, payment_method_id, 'BGN'))
        self.conn.commit()
        #self.transaction_manager.add_transaction(date, category, amount_in_BGN, transaction_type, payment_method_name, 'BGN')
        self.account_manager.update_balance(payment_method_name, amount_in_BGN, transaction_type)
        
        # Update the balance in the payment_methods table
        if transaction_type == 'Income':
            self.cursor.execute('''
                UPDATE payment_methods
                SET balance = balance + ?
                WHERE id = ?
            ''', (float(amount_in_BGN), payment_method_id))
        elif transaction_type == 'Expense':
            self.cursor.execute('''
                UPDATE payment_methods
                SET balance = balance - ?
                WHERE id = ?
            ''', (float(amount_in_BGN), payment_method_id))
        self.conn.commit()

    def remove_payment_method(self, method_name):
        if self.current_user is None:
            raise ValueError("No user logged in")
        
        self.cursor.execute('''
            SELECT id, balance FROM payment_methods
            WHERE user_id = ? AND method_name = ?
        ''', (self.current_user.user_id, method_name))
        payment_method = self.cursor.fetchone()
        
        if not payment_method:
            raise ValueError("Payment method not found")
        
        payment_method_id, balance = payment_method
        
        # Add an expense transaction for the remaining balance
        if balance > 0:
            self.add_transaction(datetime.now().date(), f"Remove Balance: {method_name}", Decimal(balance), "Expense", method_name, "BGN")

        # Remove the payment method
        self.cursor.execute('''
            DELETE FROM payment_methods
            WHERE id = ?
        ''', (payment_method_id,))
        self.conn.commit()

    def remove_transaction(self, transaction_id):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            SELECT amount, type, payment_method_id
            FROM transactions
            WHERE id = ? AND user_id = ?
        ''', (transaction_id, self.current_user.user_id))
        transaction = self.cursor.fetchone()
        if transaction:
            amount, transaction_type, payment_method_id = Decimal(transaction[0]), transaction[1], transaction[2]
            reverse_type = 'Expense' if transaction_type == 'Income' else 'Income'
            
            self.cursor.execute('''
                SELECT method_name FROM payment_methods
                WHERE id = ?
            ''', (payment_method_id,))
            payment_method_name = self.cursor.fetchone()[0]

            self.update_payment_method_balance(payment_method_name, amount, reverse_type)
            self.cursor.execute('''
                DELETE FROM transactions
                WHERE id = ? AND user_id = ?
            ''', (transaction_id, self.current_user.user_id))
            self.conn.commit()

    def update_payment_method_balance(self, method_name, amount, transaction_type):
        # Find the payment method ID
        self.cursor.execute('''
            SELECT id FROM payment_methods
            WHERE user_id = ? AND method_name = ?
        ''', (self.current_user.user_id, method_name))
        payment_method_id = self.cursor.fetchone()

        if not payment_method_id:
            raise ValueError("Payment method not found")

        payment_method_id = payment_method_id[0]

        # Update the balance in the payment_methods table
        if transaction_type == 'Income':
            self.cursor.execute('''
                UPDATE payment_methods
                SET balance = balance + ?
                WHERE id = ?
            ''', (float(amount), payment_method_id))
        elif transaction_type == 'Expense':
            self.cursor.execute('''
                UPDATE payment_methods
                SET balance = balance - ?
                WHERE id = ?
            ''', (float(amount), payment_method_id))
        self.conn.commit()

    def get_transactions(self):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            SELECT t.id, t.date, t.category, t.amount, t.type, t.currency, pm.method_name
            FROM transactions t
            JOIN payment_methods pm ON t.payment_method_id = pm.id
            WHERE t.user_id = ?
        ''', (self.current_user.user_id,))
        return self.cursor.fetchall()

    def add_goal(self, goal, target_amount, due_date):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            INSERT INTO goals (user_id, goal, target_amount, current_amount, due_date, completed)
            VALUES (?, ?, ?, ?, ?, 0)
        ''', (self.current_user.user_id, goal, float(target_amount), 0, due_date))
        self.conn.commit()

    def mark_goal_complete(self, goal_id):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            UPDATE goals
            SET completed = 1
            WHERE id = ? AND user_id = ?
        ''', (goal_id, self.current_user.user_id))
        self.conn.commit()

    def delete_goal(self, goal_id):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            DELETE FROM goals
            WHERE id = ? AND user_id = ?
        ''', (goal_id, self.current_user.user_id))
        self.conn.commit()

    def update_goal(self, goal_id, amount):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            UPDATE goals
            SET current_amount = current_amount + ?
            WHERE id = ? AND user_id = ?
        ''', (float(amount), goal_id, self.current_user.user_id))
        self.conn.commit()

    def get_goals(self):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            SELECT id, goal, target_amount, current_amount, due_date, completed
            FROM goals
            WHERE user_id = ?
        ''', (self.current_user.user_id,))
        return self.cursor.fetchall()

    def get_payment_methods(self):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            SELECT id, method_name, method_type, balance FROM payment_methods
            WHERE user_id = ?
        ''', (self.current_user.user_id,))
        return self.cursor.fetchall()

    def get_balances(self):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            SELECT SUM(CASE WHEN method_type = 'cash' THEN balance ELSE 0 END) AS cash_balance,
                SUM(CASE WHEN method_type = 'card' THEN balance ELSE 0 END) AS card_balance
            FROM payment_methods
            WHERE user_id = ?
        ''', (self.current_user.user_id,))
        balances = self.cursor.fetchone()
        cash_balance = Decimal(balances[0]) if balances[0] is not None else Decimal('0.00')
        card_balance = Decimal(balances[1]) if balances[1] is not None else Decimal('0.00')
        return {'cash': cash_balance, 'cards': {'total': card_balance}}
    
    def get_payment_methods_with_balance(self):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            SELECT method_name, method_type, ROUND(balance, 2) as rounded_balance
            FROM payment_methods
            WHERE user_id = ?
        ''', (self.current_user.user_id,))
        return self.cursor.fetchall()

    # def calculate_statistics(self, target_currency='BGN'):
    #     return self.transaction_manager.calculate_statistics(target_currency)

    # def calculate_correlations(self, target_currency='BGN'):
    #     return self.transaction_manager.calculate_correlations(target_currency)

    # def forecast(self, days_ahead=30, target_currency='BGN'):
    #     return self.transaction_manager.forecast(days_ahead, target_currency)
    
    def perform_regression_analysis(self):
        transactions = self.get_transactions(target_currency='BGN')
        dates = [pd.to_datetime(t[1]).toordinal() for t in transactions]
        amounts = [t[3] for t in transactions]
        
        X = np.array(dates).reshape(-1, 1)
        y = np.array(amounts)
        
        model = LinearRegression()
        model.fit(X, y)
        
        future_dates = np.array([pd.Timestamp('today').toordinal() + i for i in range(30)]).reshape(-1, 1)
        future_predictions = model.predict(future_dates)
        
        return future_dates, future_predictions

    def perform_clustering(self):
        transactions = self.get_transactions(target_currency='BGN')
        features = [(t[3], 1 if t[4] == 'Income' else 0) for t in transactions]
        features = np.array(features)
        
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(features)
        
        clusters = kmeans.predict(features)
        clustered_transactions = [(t, cluster) for t, cluster in zip(transactions, clusters)]
        
        return clustered_transactions

    def perform_correlation_analysis(self):
        transactions = self.get_transactions(target_currency='BGN')
        df = pd.DataFrame(transactions, columns=['ID', 'Date', 'Category', 'Amount', 'Type', 'Currency', 'Payment Method'])
        pivot_table = df.pivot_table(values='Amount', index='Date', columns='Category', aggfunc='sum').fillna(0)
        
        correlations = pivot_table.corr()
        return correlations

    def visualize_correlations(self, correlations):
        sns.heatmap(correlations, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()

    def __del__(self):
        self.conn.close()
