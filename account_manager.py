from decimal import Decimal

class AccountManager:
    def __init__(self):
        self.accounts = {'cash': Decimal('0.00'), 'cards': {}}

    def add_card(self, card_name, initial_balance):
        if not isinstance(initial_balance, Decimal):
            initial_balance = Decimal(str(initial_balance))
        self.accounts['cards'][card_name] = initial_balance

    def add_cash(self, amount):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        self.accounts['cash'] += amount

    def update_balance(self, payment_method, amount, transaction_type):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        if payment_method == 'cash':
            if transaction_type == 'Income':
                self.accounts['cash'] += amount
            elif transaction_type == 'Expense':
                self.accounts['cash'] -= amount
        elif payment_method in self.accounts['cards']:
            if transaction_type == 'Income':
                self.accounts['cards'][payment_method] += amount
            elif transaction_type == 'Expense':
                self.accounts['cards'][payment_method] -= amount
        else:
            print("Payment method not recognized.")

    def get_balances(self):
        return self.accounts

    def get_payment_methods(self):
        methods = ['cash'] + list(self.accounts['cards'].keys())
        return methods

    def add_payment_method(self, method_name, initial_balance=Decimal('0.00')):
        if method_name in self.accounts['cards']:
            print("Payment method already exists.")
        else:
            self.accounts['cards'][method_name] = Decimal(str(initial_balance))
