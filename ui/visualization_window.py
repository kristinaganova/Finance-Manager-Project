import tkinter as tk
from tkinter import ttk, messagebox

class VisualizationWindow:
    def __init__(self, root, finance_manager):
        self.root = root
        self.root.title("Reports and Charts")
        self.visualizer = finance_manager.visualizer
        self.transaction_manager = finance_manager.transaction_manager
        self.goal_manager = finance_manager.goal_manager

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(main_frame, text="Visualize Data", command=self.visualize_data).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(main_frame, text="Visualize Forecast", command=self.visualize_forecast).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Visualize Statistics", command=self.visualize_statistics).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(main_frame, text="Visualize Goal Progress", command=self.visualize_goal_progress).grid(row=0, column=3, padx=5, pady=5)

    def visualize_data(self):
        try:
            # Assuming the data visualization logic exists
            self.visualizer.visualize_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_forecast(self):
        try:
            future_expenses, future_income = self.transaction_manager.forecast()
            self.visualizer.visualize_forecast(future_expenses, future_income)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_statistics(self):
        try:
            stats = self.transaction_manager.calculate_statistics()
            self.visualizer.visualize_statistics(stats)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_goal_progress(self):
        try:
            goal_progress = self.goal_manager.calculate_goal_progress()
            self.visualizer.visualize_goal_progress(goal_progress)
        except Exception as e:
            messagebox.showerror("Error", str(e))
