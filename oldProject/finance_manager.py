import pickle
from transaction_manager import TransactionManager
from account_manager import AccountManager
from goal_manager import GoalManager
from currency_converter import CurrencyConverter
from visualizer import Visualizer
from decimal import Decimal
from datetime import datetime

class FinanceManager:
    def __init__(self):
        self.currency_converter = CurrencyConverter()
        self.transaction_manager = TransactionManager(self.currency_converter)
        self.account_manager = AccountManager()
        self.goal_manager = GoalManager()

    def add_transaction(self, date, category, amount, transaction_type, payment_method, currency='BGN'):
        amount_in_BGN = self.currency_converter.convert_currency(amount, currency, 'BGN')
        self.transaction_manager.add_transaction(date, category, amount_in_BGN, transaction_type, payment_method, 'BGN')
        self.account_manager.update_balance(payment_method, amount_in_BGN, transaction_type)

    def remove_transaction(self, index):
        if index in self.transaction_manager.get_transactions().index:
            transaction = self.transaction_manager.get_transactions().iloc[index]
            amount = transaction['Amount']
            transaction_type = transaction['Type']
            payment_method = transaction['Payment Method']
            self.account_manager.update_balance(payment_method, -amount if transaction_type == 'Income' else amount, transaction_type)
            self.transaction_manager.remove_transaction(index)
        else:
            print("Transaction not found.")

    def add_goal(self, goal, target_amount, due_date):
        self.goal_manager.add_goal(goal, target_amount, due_date)

    def update_goal(self, index, amount):
        self.goal_manager.update_goal(index, amount)

    def get_transactions(self, target_currency='BGN'):
        return self.transaction_manager.get_transactions(target_currency)

    def get_goals(self):
        return self.goal_manager.get_goals()

    def get_balances(self):
        return self.account_manager.get_balances()

    def calculate_statistics(self, target_currency='BGN'):
        return self.transaction_manager.calculate_statistics(target_currency)

    def calculate_correlations(self, target_currency='BGN'):
        return self.transaction_manager.calculate_correlations(target_currency)

    def forecast(self, days_ahead=30, target_currency='BGN'):
        return self.transaction_manager.forecast(days_ahead, target_currency)

    def visualize_data(self, target_currency='BGN'):
        visualizer = Visualizer(self.transaction_manager.get_transactions(target_currency))
        visualizer.visualize_data()

    def visualize_forecast(self, future_expenses, future_income):
        visualizer = Visualizer(self.transaction_manager.get_transactions())
        visualizer.visualize_forecast(future_expenses, future_income)

    def get_payment_methods(self):
        return self.account_manager.get_payment_methods()

    def add_payment_method(self, method_name, initial_balance=Decimal('0.00')):
        self.account_manager.add_payment_method(method_name, initial_balance)

    def save_data(self, filename='finance_data.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_data(filename='finance_data.pkl'):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return FinanceManager()