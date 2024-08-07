import tkinter as tk
from tkinter import ttk, messagebox
from finance_manager import FinanceManager
from decimal import Decimal
from datetime import datetime
from tkcalendar import DateEntry

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Manager")

        # Зареждане на данни
        self.finance_manager = FinanceManager.load_data()

        self.create_widgets()

        # Съхраняване на данни при затваряне на прозореца
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Основен прозорец
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Общо налични пари:").grid(row=0, column=0, padx=10, pady=10)
        self.total_balance_label = ttk.Label(main_frame, text=str(self.calculate_total_balance()))
        self.total_balance_label.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(main_frame, text="Налични в кеш:").grid(row=1, column=0, padx=10, pady=10)
        self.cash_balance_label = ttk.Label(main_frame, text=str(self.finance_manager.get_balances()['cash']))
        self.cash_balance_label.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(main_frame, text="Налични по карти:").grid(row=2, column=0, padx=10, pady=10)
        self.cards_balance_label = ttk.Label(main_frame, text=str(self.calculate_total_card_balance()))
        self.cards_balance_label.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(main_frame, text="Управление на Транзакции", command=self.open_transaction_window).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(main_frame, text="Управление на Цели", command=self.open_goal_window).grid(row=3, column=1, padx=10, pady=10)
        ttk.Button(main_frame, text="Справки и Диаграми", command=self.open_visualization_window).grid(row=3, column=2, padx=10, pady=10)

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
        TransactionWindow(transaction_window, self.finance_manager)

    def open_goal_window(self):
        goal_window = tk.Toplevel(self.root)
        GoalWindow(goal_window, self.finance_manager)

    def open_visualization_window(self):
        visualization_window = tk.Toplevel(self.root)
        VisualizationWindow(visualization_window, self.finance_manager)

    def on_closing(self):
        self.finance_manager.save_data()
        self.root.destroy()

class TransactionWindow:
    def __init__(self, root, finance_manager):
        self.root = root
        self.root.title("Управление на Транзакции")
        self.finance_manager = finance_manager

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame for adding transactions
        frame_transactions = ttk.LabelFrame(main_frame, text="Add Transaction")
        frame_transactions.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_transactions, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(frame_transactions, date_pattern='yyyy-mm-dd', width=12)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_transactions, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.category_entry = ttk.Entry(frame_transactions, width=12)
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_transactions, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(frame_transactions, width=12)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_transactions, text="Type:").grid(row=1, column=2, padx=5, pady=5)
        self.type_combobox = ttk.Combobox(frame_transactions, values=["Income", "Expense"], width=10)
        self.type_combobox.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(frame_transactions, text="Payment Method:").grid(row=2, column=0, padx=5, pady=5)
        self.payment_method_combobox = ttk.Combobox(frame_transactions, state="readonly")
        self.payment_method_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.update_payment_methods_combobox()

        ttk.Label(frame_transactions, text="Currency:").grid(row=2, column=2, padx=5, pady=5)
        self.currency_entry = ttk.Entry(frame_transactions, width=12)
        self.currency_entry.grid(row=2, column=3, padx=5, pady=5)

        ttk.Button(frame_transactions, text="Add Transaction", command=self.add_transaction).grid(row=3, column=0, columnspan=4, padx=5, pady=5)

        # Frame for displaying transactions
        frame_display = ttk.LabelFrame(main_frame, text="Transactions")
        frame_display.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.transactions_tree = ttk.Treeview(frame_display, columns=("Payment Method", "Currency", "Date", "Category", "Amount", "Type"), show="headings", height=5)
        self.transactions_tree.heading("Date", text="Date")
        self.transactions_tree.heading("Category", text="Category")
        self.transactions_tree.heading("Amount", text="Amount")
        self.transactions_tree.heading("Type", text="Type")
        self.transactions_tree.heading("Payment Method", text="Payment Method")
        self.transactions_tree.heading("Currency", text="Currency")
        self.transactions_tree.grid(row=0, column=0, padx=5, pady=5)
        self.transactions_tree.column("Date", width=80)
        self.transactions_tree.column("Category", width=80)
        self.transactions_tree.column("Amount", width=80)
        self.transactions_tree.column("Type", width=80)
        self.transactions_tree.column("Payment Method", width=100)
        self.transactions_tree.column("Currency", width=80)

        self.update_transactions_tree()

        ttk.Button(frame_display, text="Delete Transaction", command=self.delete_transaction).grid(row=1, column=0, padx=5, pady=5)

    def add_transaction(self):
        try:
            date = self.date_entry.get_date()
            category = self.category_entry.get()
            amount = Decimal(self.amount_entry.get())
            transaction_type = self.type_combobox.get()
            payment_method = self.payment_method_combobox.get()
            currency = self.currency_entry.get()
            self.finance_manager.add_transaction(date, category, amount, transaction_type, payment_method, currency)
            self.update_transactions_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_transaction(self):
        try:
            selected_item = self.transactions_tree.selection()[0]
            transaction_index = self.transactions_tree.index(selected_item)
            self.finance_manager.remove_transaction(transaction_index)
            self.update_transactions_tree()
        except IndexError:
            messagebox.showerror("Error", "No transaction selected")

    def update_transactions_tree(self):
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
        for index, row in self.finance_manager.get_transactions().iterrows():
            self.transactions_tree.insert("", "end", values=row.tolist())

    def update_payment_methods_combobox(self):
        self.payment_method_combobox['values'] = self.finance_manager.get_payment_methods()


class GoalWindow:
    def __init__(self, root, finance_manager):
        self.root = root
        self.root.title("Управление на Цели")
        self.finance_manager = finance_manager

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame for adding goals
        frame_goals = ttk.LabelFrame(main_frame, text="Add Goal")
        frame_goals.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_goals, text="Goal:").grid(row=0, column=0, padx=5, pady=5)
        self.goal_entry = ttk.Entry(frame_goals, width=12)
        self.goal_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_goals, text="Target Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.target_amount_entry = ttk.Entry(frame_goals, width=12)
        self.target_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_goals, text="Due Date:").grid(row=2, column=0, padx=5, pady=5)
        self.due_date_entry = DateEntry(frame_goals, date_pattern='yyyy-mm-dd', width=12)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_goals, text="Add Goal", command=self.add_goal).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Frame for displaying goals
        frame_display = ttk.LabelFrame(main_frame, text="Goals")
        frame_display.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.goals_tree = ttk.Treeview(frame_display, columns=("Goal", "Target Amount", "Current Amount", "Due Date"), show="headings", height=5)
        self.goals_tree.heading("Goal", text="Goal")
        self.goals_tree.heading("Target Amount", text="Target Amount")
        self.goals_tree.heading("Current Amount", text="Current Amount")
        self.goals_tree.heading("Due Date", text="Due Date")
        self.goals_tree.grid(row=0, column=0, padx=5, pady=5)
        self.goals_tree.column("Goal", width=100)
        self.goals_tree.column("Target Amount", width=100)
        self.goals_tree.column("Current Amount", width=100)
        self.goals_tree.column("Due Date", width=100)

        self.update_goals_tree()

    def add_goal(self):
        try:
            goal = self.goal_entry.get()
            target_amount = Decimal(self.target_amount_entry.get())
            due_date = self.due_date_entry.get_date()
            self.finance_manager.add_goal(goal, target_amount, due_date)
            self.update_goals_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_goals_tree(self):
        for item in self.goals_tree.get_children():
            self.goals_tree.delete(item)
        for _, row in self.finance_manager.get_goals().iterrows():
            self.goals_tree.insert("", "end", values=row.tolist())

class VisualizationWindow:
    def __init__(self, root, finance_manager):
        self.root = root
        self.root.title("Справки и Диаграми")
        self.finance_manager = finance_manager

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(main_frame, text="Visualize Data", command=self.visualize_data).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(main_frame, text="Visualize Forecast", command=self.visualize_forecast).grid(row=0, column=1, padx=5, pady=5)

    def visualize_data(self):
        try:
            self.finance_manager.visualize_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_forecast(self):
        try:
            future_expenses, future_income = self.finance_manager.forecast()
            self.finance_manager.visualize_forecast(future_expenses, future_income)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
