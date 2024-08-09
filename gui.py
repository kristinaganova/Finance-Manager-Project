import tkinter as tk
from tkinter import ttk, messagebox
from finance_manager import FinanceManager
from user import User
from decimal import Decimal
from transaction_window import TransactionWindow
from goal_window import GoalWindow
from visualization_window import VisualizationWindow
from initialize_database import initialize_database
from payment_method_window import PaymentMethodsWindow

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Manager")

        # Load data
        self.finance_manager = FinanceManager()

        self.create_login_widgets()

    def create_login_widgets(self):
        login_frame = ttk.Frame(self.root)
        login_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(login_frame, width=20)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", width=20)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(login_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = User.login_user(username, password)
        if user:
            self.finance_manager.set_user(user)
            self.clear_login_widgets()
            self.create_main_widgets()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = User.register_user(username, password)
        if user:
            messagebox.showinfo("Success", "User registered successfully")
            self.finance_manager.set_user(user)
            self.clear_login_widgets()
            self.create_main_widgets()
        else:
            messagebox.showerror("Error", "Username already exists")

    def clear_login_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_widgets(self):
        # Main window
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Total Balance:").grid(row=0, column=0, padx=10, pady=10)
        self.total_balance_label = ttk.Label(main_frame, text=str(round(self.calculate_total_balance(), 2)))
        self.total_balance_label.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(main_frame, text="Cash Balance:").grid(row=1, column=0, padx=10, pady=10)
        self.cash_balance_label = ttk.Label(main_frame, text=str(round(self.finance_manager.get_balances()['cash'], 2)))
        self.cash_balance_label.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(main_frame, text="Card Balance:").grid(row=2, column=0, padx=10, pady=10)
        self.cards_balance_label = ttk.Label(main_frame, text=str(round(self.calculate_total_card_balance(), 2)))
        self.cards_balance_label.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(main_frame, text="Manage Transactions", command=self.open_transaction_window).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(main_frame, text="Manage Goals", command=self.open_goal_window).grid(row=3, column=1, padx=10, pady=10)
        ttk.Button(main_frame, text="Reports and Charts", command=self.open_visualization_window).grid(row=3, column=2, padx=10, pady=10)
        ttk.Button(main_frame, text="Manage Payment Methods", command=self.open_payment_methods_window).grid(row=3, column=3, padx=10, pady=10)

        self.refresh_ui()

    def refresh_ui(self):
        self.total_balance_label.config(text=str(round(self.calculate_total_balance(), 2)))
        self.cash_balance_label.config(text=str(round(self.finance_manager.get_balances()['cash'], 2)))
        self.cards_balance_label.config(text=str(round(self.calculate_total_card_balance(), 2)))

    def calculate_total_balance(self):
        balances = self.finance_manager.get_balances()
        total = balances['cash'] + sum(balances['cards'].values())
        return total

    def calculate_total_card_balance(self):
        balances = self.finance_manager.get_balances()
        total = sum(balances['cards'].values())
        return total

    def open_transaction_window(self):
        transaction_window = tk.Toplevel(self.root)
        TransactionWindow(transaction_window, self.finance_manager, self.refresh_ui)

    def open_goal_window(self):
        goal_window = tk.Toplevel(self.root)
        GoalWindow(goal_window, self.finance_manager)

    def open_visualization_window(self):
        visualization_window = tk.Toplevel(self.root)
        VisualizationWindow(visualization_window, self.finance_manager)

    def open_payment_methods_window(self):
        payment_methods_window = tk.Toplevel(self.root)
        PaymentMethodsWindow(payment_methods_window, self.finance_manager, self.refresh_ui)

if __name__ == "__main__":
    initialize_database()  # Ensure database is initialized
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
