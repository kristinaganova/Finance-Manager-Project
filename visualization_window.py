import tkinter as tk
from tkinter import ttk, messagebox

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
