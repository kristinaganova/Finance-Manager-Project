import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from decimal import Decimal
from datetime import datetime

class TransactionWindow:
    def __init__(self, root, transaction_manager, account_manager, refresh_ui_callback):
        self.root = root
        self.root.title("Manage Transactions")
        self.transaction_manager = transaction_manager
        self.account_manager = account_manager
        self.refresh_ui_callback = refresh_ui_callback

        self.create_widgets()

    # Rest of the code remains the same

    def update_payment_methods_combobox(self):
        payment_methods = self.account_manager.get_payment_methods()
        self.payment_method_combobox['values'] = payment_methods


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

        self.transactions_tree = ttk.Treeview(frame_display, columns=("ID", "Date", "Category", "Amount", "Type", "Currency", "Payment Method"), show="headings", height=5)
        self.transactions_tree.heading("ID", text="ID")
        self.transactions_tree.heading("Date", text="Date")
        self.transactions_tree.heading("Category", text="Category")
        self.transactions_tree.heading("Amount", text="Amount")
        self.transactions_tree.heading("Type", text="Type")
        self.transactions_tree.heading("Currency", text="Currency")
        self.transactions_tree.heading("Payment Method", text="Payment Method")
        self.transactions_tree.grid(row=0, column=0, padx=5, pady=5)
        self.transactions_tree.column("ID", width=30)
        self.transactions_tree.column("Date", width=80)
        self.transactions_tree.column("Category", width=80)
        self.transactions_tree.column("Amount", width=80)
        self.transactions_tree.column("Type", width=80)
        self.transactions_tree.column("Currency", width=80)
        self.transactions_tree.column("Payment Method", width=100)

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
            self.transaction_manager.add_transaction(date, category, amount, transaction_type, payment_method, currency)
            self.update_transactions_tree()  # Update the transactions tree after adding a transaction
            self.refresh_ui_callback()  # Refresh the main UI
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_transaction(self):
        try:
            selected_item = self.transactions_tree.selection()[0]
            transaction_id = self.transactions_tree.item(selected_item)['values'][0]
            self.transaction_manager.remove_transaction(transaction_id)
            self.update_transactions_tree()  # Update the transactions tree after deleting a transaction
            self.refresh_ui_callback()  # Refresh the main UI
        except IndexError:
            messagebox.showerror("Error", "No transaction selected")

    def update_transactions_tree(self):
        # Clear existing rows
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        # Populate with current transactions
        transactions_df = self.transaction_manager.get_transactions()
        for index, row in transactions_df.iterrows():
            self.transactions_tree.insert("", "end", values=(row['ID'], row['Date'], row['Category'], row['Amount'], row['Type'], row['Currency'], row['Payment Method']))