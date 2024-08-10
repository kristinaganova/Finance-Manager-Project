import sqlite3
from .currency_converter import CurrencyConverter
from .account_manager import AccountManager
from .transaction_manager import TransactionManager
from .goal_manager import GoalManager
from .user import User
from utils.initialize_database import DATABASE_PATH

class FinanceManager:
    def __init__(self, db_path=DATABASE_PATH):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.current_user = None
        self.account_manager = None
        self.transaction_manager = None
        self.goal_manager = None
        self.currency_converter = CurrencyConverter()

    def set_user(self, user):
        self.current_user = user
        self.account_manager = AccountManager(self.conn, self.current_user)
        self.transaction_manager = TransactionManager(self.conn, self.current_user, self.account_manager, self.currency_converter)
        self.goal_manager = GoalManager(self.conn, self.current_user)

    def get_goals(self):
        if self.goal_manager:
            return self.goal_manager.get_goals()
        else:
            return []
        
    def get_balances(self):
        return self.account_manager.get_balances()

    def add_payment_method(self, method_name, method_type, initial_balance):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.account_manager.add_payment_method(method_name, method_type, initial_balance)

    def add_transaction(self, date, category, amount, transaction_type, payment_method_name, currency='BGN'):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.transaction_manager.add_transaction(date, category, amount, transaction_type, payment_method_name, currency)

    def remove_payment_method(self, method_name):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.account_manager.remove_payment_method(method_name)

    def add_goal(self, goal, target_amount, due_date):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.goal_manager.add_goal(goal, target_amount, due_date)

    def mark_goal_complete(self, goal_id):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.goal_manager.mark_goal_complete(goal_id)

    def delete_goal(self, goal_id):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.goal_manager.delete_goal(goal_id)

    def update_goal(self, goal_id, amount):
        if self.current_user is None:
            raise ValueError("No user logged in")
        self.goal_manager.update_goal(goal_id, amount)

    def generate_statistics_report(self):
        stats = self.transaction_manager.calculate_statistics()
        correlations = self.transaction_manager.calculate_correlations()
        future_expenses, future_income = self.transaction_manager.forecast()
        goal_progress = self.goal_manager.calculate_goal_progress()
        goal_forecasts = self.goal_manager.forecast_goal_completion()

        report = {
            "Transaction Statistics": stats,
            "Correlations": correlations,
            "Future Forecast": {
                "Expenses": future_expenses,
                "Income": future_income
            },
            "Goal Progress": goal_progress.to_dict('records'),
            "Goal Forecasts": goal_forecasts.to_dict('records')
        }

        return report

    def __del__(self):
        if self.conn:
            self.conn.close()