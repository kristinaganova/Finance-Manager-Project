import tkinter as tk
from tkinter import ttk, messagebox

class VisualizationWindow:
    def __init__(self, root, finance_manager):
        self.root = root
        self.root.title("Reports and Charts")
        self.visualizer = finance_manager.visualizer
        self.transaction_manager = finance_manager.transaction_manager
        self.goal_manager = finance_manager.goal_manager
        self.account_manager = finance_manager.account_manager  # Added for extended correlations

        self.create_widgets()

#TO DO:
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(main_frame, text="Visualize Data", command=self.visualize_statistics).grid(row=0, column=0, padx=5, pady=5)
        #ttk.Button(main_frame, text="Visualize Forecast", command=self.visualize_forecast).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Visualize Distribution", command=self.visualize_distribution).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(main_frame, text="Time Series Analysis", command=self.visualize_time_series).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(main_frame, text="Category Comparison", command=self.visualize_category_comparison).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(main_frame, text="Extended Correlations", command=self.visualize_extended_correlations).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(main_frame, text="Goal Progress", command=self.visualize_goal_progress).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(main_frame, text="Goal Gauge", command=self.visualize_goal_gauge).grid(row=0, column=7, padx=5, pady=5)
        ttk.Button(main_frame, text="Transaction Clusters", command=self.visualize_clusters).grid(row=0, column=8, padx=5, pady=5)

    def visualize_statistics(self):
        try:
            stats = self.transaction_manager.calculate_statistics()
            self.visualizer.visualize_statistics(stats)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_distribution(self):
        try:
            transactions = self.transaction_manager.get_transactions()
            self.visualizer.visualize_distribution(transactions, 'Expenses', 'Amount')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_time_series(self):
        try:
            transactions = self.transaction_manager.get_transactions()
            self.visualizer.visualize_time_series(transactions)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_category_comparison(self):
        try:
            transactions = self.transaction_manager.get_transactions()
            self.visualizer.visualize_category_comparison(transactions)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_extended_correlations(self):
        try:
            transactions = self.transaction_manager.get_transactions()
            balances = self.account_manager.get_balances()
            self.visualizer.visualize_extended_correlations(transactions, balances)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_goal_progress(self):
        try:
            goal_progress = self.goal_manager.calculate_goal_progress()
            self.visualizer.visualize_goal_progress(goal_progress)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_goal_gauge(self):
        try:
            goals_df = self.goal_manager.get_goals()
            for _, row in goals_df.iterrows():
                self.visualizer.visualize_goal_gauge(row['Goal'], row['Target Amount'], row['Current Amount'])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_clusters(self):
        try:
            transactions = self.transaction_manager.get_transactions()
            self.visualizer.visualize_clusters(transactions)
        except Exception as e:
            messagebox.showerror("Error", str(e))
