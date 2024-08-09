from decimal import Decimal
import sqlite3
from utils.initialize_database import DATABASE_PATH

class AccountManager:
    def __init__(self, conn, user):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.user = user
        self.accounts = {'cards': {}, 'cash': {}}
        self.load_accounts()

    def set_user(self, user):
        self.user = user
        self.load_accounts()

    def load_accounts(self):
        self.cursor.execute('''
            SELECT method_name, method_type, balance
            FROM payment_methods
            WHERE user_id = ?
        ''', (self.user.user_id,))
        methods = self.cursor.fetchall()

        for method_name, method_type, balance in methods:
            if method_type == 'cash':
                self.accounts['cash'][method_name] = Decimal(balance)
            elif method_type == 'card':
                self.accounts['cards'][method_name] = Decimal(balance)

    def get_payment_methods_with_balance(self):
        payment_methods = []
        for method_name, balance in self.accounts['cash'].items():
            payment_methods.append((method_name, 'cash', balance))
        for method_name, balance in self.accounts['cards'].items():
            payment_methods.append((method_name, 'card', balance))

        return payment_methods

    def add_payment_method(self, method_name, method_type, initial_balance=Decimal('0.00')):
        if not isinstance(initial_balance, Decimal):
            initial_balance = Decimal(str(initial_balance))

        if method_type == 'cash':
            if method_name in self.accounts['cash']:
                raise ValueError("Payment method already exists.")
            self.accounts['cash'][method_name] = initial_balance
        elif method_type == 'card':
            if method_name in self.accounts['cards']:
                raise ValueError("Payment method already exists.")
            self.accounts['cards'][method_name] = initial_balance
        else:
            raise ValueError("Invalid payment method type.")

        self._store_payment_method_in_db(method_name, method_type, initial_balance)

    def remove_payment_method(self, method_name):
        if method_name in self.accounts['cash']:
            # Просто премахваме метода и свързания баланс
            del self.accounts['cash'][method_name]
        elif method_name in self.accounts['cards']:
            # Просто премахваме метода и свързания баланс
            del self.accounts['cards'][method_name]
        else:
            raise ValueError("Payment method not found.")

        # Премахване на метода от базата данни
        self._remove_payment_method_from_db(method_name)


    def update_balance(self, payment_method, amount, transaction_type):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        if payment_method in self.accounts['cash']:
            self._update_cash_balance(payment_method, amount, transaction_type)
        elif payment_method in self.accounts['cards']:
            self._update_card_balance(payment_method, amount, transaction_type)
        else:
            raise ValueError("Payment method not recognized.")

    def _store_payment_method_in_db(self, method_name, method_type, balance):
        if self.user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            INSERT INTO payment_methods (user_id, method_name, method_type, balance)
            VALUES (?, ?, ?, ?)
        ''', (self.user.user_id, method_name, method_type, float(balance)))
        self.conn.commit()

    def _remove_payment_method_from_db(self, method_name):
        if self.user is None:
            raise ValueError("No user logged in")
        self.cursor.execute('''
            DELETE FROM payment_methods WHERE user_id = ? AND method_name = ?
        ''', (self.user.user_id, method_name))
        self.conn.commit()

    def _update_cash_balance(self, payment_method, amount, transaction_type):
        if transaction_type == 'Income':
            self.accounts['cash'][payment_method] += amount
        elif transaction_type == 'Expense':
            self.accounts['cash'][payment_method] -= amount
        else:
            raise ValueError("Invalid transaction type.")

    def _update_card_balance(self, payment_method, amount, transaction_type):
        if transaction_type == 'Income':
            self.accounts['cards'][payment_method] += amount
        elif transaction_type == 'Expense':
            self.accounts['cards'][payment_method] -= amount
        else:
            raise ValueError("Invalid transaction type.")

    def get_balances(self):
        return self.accounts

    def get_payment_methods(self):
        payment_methods = list(self.accounts['cash'].keys()) + list(self.accounts['cards'].keys())
        return payment_methods
