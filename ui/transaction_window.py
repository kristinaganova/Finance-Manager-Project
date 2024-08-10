import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from decimal import Decimal
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import pandas as pd

class TransactionWindow:
    def __init__(self, root, transaction_manager, account_manager, refresh_ui_callback):
        self.root = root
        self.root.title("Manage Transactions")
        self.transaction_manager = transaction_manager
        self.account_manager = account_manager
        self.refresh_ui_callback = refresh_ui_callback

        self.create_widgets()

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

        ttk.Button(frame_display, text="Delete Transaction", command=self.delete_transaction).grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        # Visualize Buttons in a separate frame
        frame_visualization = ttk.LabelFrame(main_frame, text="Visualizations")
        frame_visualization.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(frame_visualization, text="Visualize Income vs Expense", command=self.visualize_income_vs_expense).grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(frame_visualization, text="Visualize Transaction Statistics", command=self.visualize_statistics).grid(row=4, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(frame_visualization, text="Transaction Clusters", command=self.visualize_clusters).grid(row=5, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(frame_visualization, text="Category Comparison", command=self.visualize_category_comparison).grid(row=6, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(frame_visualization, text="Time Series", command=self.visualize_time_series).grid(row=7, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(frame_visualization, text="Distribution", command=self.visualize_distribution).grid(row=8, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(frame_visualization, text="Forecast", command=self.vizualize_forecast).grid(row=9, column=0, padx=5, pady=5, sticky='ew')


    def add_transaction(self):
        try:
            date = self.date_entry.get_date()
            category = self.category_entry.get()
            amount = Decimal(self.amount_entry.get())
            transaction_type = self.type_combobox.get()
            payment_method = self.payment_method_combobox.get()
            currency = self.currency_entry.get()

            if not category or not amount or not transaction_type or not payment_method or not currency:
                raise ValueError("All fields must be filled out.")
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
            
            self.transaction_manager.add_transaction(date, category, amount, transaction_type, payment_method, currency)
            self.update_transactions_tree()
            self.refresh_ui_callback()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_transaction(self):
        try:
            selected_item = self.transactions_tree.selection()[0]
            transaction_id = self.transactions_tree.item(selected_item)['values'][0]
            self.transaction_manager.remove_transaction(transaction_id)
            self.update_transactions_tree()  
            self.refresh_ui_callback()  
        except IndexError:
            messagebox.showerror("Error", "No transaction selected")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_transactions_tree(self):
        try:
            for item in self.transactions_tree.get_children():
                self.transactions_tree.delete(item)

            transactions_df = self.transaction_manager.get_transactions()
            for index, row in transactions_df.iterrows():
                self.transactions_tree.insert("", "end", values=(row['ID'], row['Date'], row['Category'], row['Amount'], row['Type'], row['Currency'], row['Payment Method']))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_income_vs_expense(self):
        try:
            transactions = self.transaction_manager.get_transactions()
            income_total = transactions[transactions['Type'] == 'Income']['Amount'].sum()
            expense_total = transactions[transactions['Type'] == 'Expense']['Amount'].sum()

            labels = ['Income', 'Expense']
            sizes = [income_total, expense_total]
            colors = ['#66b3ff', '#ff6666']

            plt.figure(figsize=(8, 8))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.title('Income vs. Expense')
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_statistics(self):
        try:
            stats = self.transaction_manager.calculate_statistics()
            categories = list(stats.keys())
            values = list(stats.values())

            plt.figure(figsize=(10, 5))
            plt.bar(categories, values, color='skyblue')
            plt.title('Transaction Statistics')
            plt.xlabel('Statistics')
            plt.ylabel('Value')
            plt.xticks(rotation=45)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_clusters(self):
        try:
            transactions = self.transaction_manager.get_transactions()
            transactions['Date'] = pd.to_datetime(transactions['Date'])
            features = transactions[['Amount']]
            kmeans = KMeans(n_clusters=3)
            transactions['Cluster'] = kmeans.fit_predict(features)
            
            plt.figure(figsize=(10, 5))
            sns.scatterplot(x='Date', y='Amount', hue='Cluster', data=transactions, palette='Set1')
            plt.title('Transaction Clusters')
            plt.xlabel('Date')
            plt.ylabel('Amount')
            plt.xticks(rotation=45)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_category_comparison(self):
        try:
            plt.figure(figsize=(12, 6))
            transactions = self.transaction_manager.get_transactions()
            sns.boxplot(x='Category', y='Amount', data=transactions[transactions['Type'] == 'Expense'])
            plt.title('Expense Distribution by Category')
            plt.xlabel('Category')
            plt.ylabel('Amount')
            plt.xticks(rotation=45)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_time_series(self):
        try:
            transactions = self.transaction_manager.get_transactions()
            transactions['Date'] = pd.to_datetime(transactions['Date'])
            plt.figure(figsize=(12, 6))
            sns.lineplot(x='Date', y='Amount', hue='Type', data=transactions)
            plt.title('Time Series of Transactions')
            plt.xlabel('Date')
            plt.ylabel('Amount')
            plt.xticks(rotation=45)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def visualize_distribution(self, title='Expenses', column='Amount'):
        try:
            plt.figure(figsize=(10, 5))
            transactions = self.transaction_manager.get_transactions()
            sns.histplot(transactions[column], kde=True, color='blue', bins=30)
            plt.title(f'Distribution of {title}')
            plt.xlabel('Amount')
            plt.ylabel('Frequency')
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def vizualize_forecast(self):
        try:
            future_expenses, future_income = self.transaction_manager.forecast()

            dates = pd.date_range(start=datetime.now(), periods=len(future_expenses), freq='D')

            plt.figure(figsize=(10, 5))
            plt.plot(dates, future_expenses, label='Forecasted Expenses', color='red')
            plt.plot(dates, future_income, label='Forecasted Income', color='green')
            plt.title('Income and Expenses Forecast')
            plt.xlabel('Date')
            plt.ylabel('Amount')
            plt.legend()
            plt.grid(True)
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", str(e))