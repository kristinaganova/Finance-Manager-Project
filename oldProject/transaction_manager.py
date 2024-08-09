import pandas as pd
from decimal import Decimal
from datetime import datetime, timedelta

class TransactionManager:
    def __init__(self, currency_converter):
        self.transactions = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Type', 'Currency', 'Payment Method'])
        self.currency_converter = currency_converter

    def add_transaction(self, date, category, amount, transaction_type, payment_method, currency='USD'):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        new_transaction = pd.DataFrame({
            'Date': [date], 
            'Category': [category], 
            'Amount': [amount], 
            'Type': [transaction_type], 
            'Currency': [currency], 
            'Payment Method': [payment_method]
        })
        self.transactions = pd.concat([self.transactions, new_transaction], ignore_index=True)

    def remove_transaction(self, index):
        if index in self.transactions.index:
            self.transactions = self.transactions.drop(index)
        else:
            print("Transaction not found.")

    def get_transactions(self, target_currency='USD'):
        if target_currency == 'USD':
            return self.transactions
        converted_transactions = self.transactions.copy()
        converted_transactions['Amount'] = converted_transactions.apply(
            lambda row: self.currency_converter.convert_currency(row['Amount'], row['Currency'], target_currency), axis=1)
        converted_transactions['Currency'] = target_currency
        return converted_transactions

    def calculate_statistics(self, target_currency='USD'):
        transactions = self.get_transactions(target_currency)
        expenses = transactions[transactions['Type'] == 'Expense']['Amount']
        income = transactions[transactions['Type'] == 'Income']['Amount']
        stats = {
            'Mean Expense': sum(expenses, Decimal(0)) / len(expenses) if len(expenses) > 0 else Decimal(0),
            'Median Expense': sorted(expenses)[len(expenses) // 2] if len(expenses) > 0 else Decimal(0),
            'Std Dev Expense': (sum((x - (sum(expenses, Decimal(0)) / len(expenses))) ** 2 for x in expenses) / len(expenses)).sqrt() if len(expenses) > 0 else Decimal(0),
            'Mean Income': sum(income, Decimal(0)) / len(income) if len(income) > 0 else Decimal(0),
            'Median Income': sorted(income)[len(income) // 2] if len(income) > 0 else Decimal(0),
            'Std Dev Income': (sum((x - (sum(income, Decimal(0)) / len(income))) ** 2 for x in income) / len(income)).sqrt() if len(income) > 0 else Decimal(0),
        }
        return stats

    def calculate_correlations(self, target_currency='USD'):
        transactions = self.get_transactions(target_currency)
        expenses = transactions[transactions['Type'] == 'Expense']
        expenses_by_category = expenses.pivot_table(values='Amount', index='Date', columns='Category', aggfunc='sum', fill_value=Decimal(0))
        correlations = expenses_by_category.corr()
        return correlations

    def forecast(self, days_ahead=30, target_currency='USD'):
        transactions = self.get_transactions(target_currency)
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