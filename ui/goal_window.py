import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from decimal import Decimal
import matplotlib.pyplot as plt

class GoalWindow:
    def __init__(self, root, finance_manager, refresh_ui_callback):
        self.root = root
        self.root.title("Manage Goals")
        self.goal_manager = finance_manager.goal_manager
        self.account_manager = finance_manager.account_manager
        self.refresh_ui_callback = refresh_ui_callback  # Ensure we can refresh the UI

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

        ttk.Label(frame_goals, text="Initial Deposit:").grid(row=3, column=0, padx=5, pady=5)
        self.initial_deposit_entry = ttk.Entry(frame_goals, width=12)
        self.initial_deposit_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame_goals, text="From Payment Method:").grid(row=4, column=0, padx=5, pady=5)
        self.payment_method_combobox = ttk.Combobox(frame_goals, values=self.account_manager.get_payment_methods(), state="readonly", width=12)
        self.payment_method_combobox.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(frame_goals, text="Add Goal", command=self.add_goal).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Frame for adding money to an existing goal
        frame_add_money = ttk.LabelFrame(main_frame, text="Add Money to Goal")
        frame_add_money.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_add_money, text="Goal ID:").grid(row=0, column=0, padx=5, pady=5)
        self.goal_id_entry = ttk.Entry(frame_add_money, width=12)
        self.goal_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_add_money, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(frame_add_money, width=12)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_add_money, text="From Payment Method:").grid(row=2, column=0, padx=5, pady=5)
        self.add_payment_method_combobox = ttk.Combobox(frame_add_money, values=self.account_manager.get_payment_methods(), state="readonly", width=12)
        self.add_payment_method_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_add_money, text="Add Money", command=self.add_money_to_goal).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Frame for displaying goals
        frame_display = ttk.LabelFrame(main_frame, text="Goals")
        frame_display.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.goals_tree = ttk.Treeview(frame_display, columns=("ID", "Goal", "Target Amount", "Current Amount", "Due Date", "Completed"), show="headings", height=5)
        self.goals_tree.heading("ID", text="ID")
        self.goals_tree.heading("Goal", text="Goal")
        self.goals_tree.heading("Target Amount", text="Target Amount")
        self.goals_tree.heading("Current Amount", text="Current Amount")
        self.goals_tree.heading("Due Date", text="Due Date")
        self.goals_tree.heading("Completed", text="Completed")
        self.goals_tree.grid(row=0, column=0, padx=5, pady=5)
        self.goals_tree.column("ID", width=50)
        self.goals_tree.column("Goal", width=100)
        self.goals_tree.column("Target Amount", width=100)
        self.goals_tree.column("Current Amount", width=100)
        self.goals_tree.column("Due Date", width=100)
        self.goals_tree.column("Completed", width=100)

        self.update_goals_tree()

        ttk.Button(frame_display, text="Delete Goal", command=self.delete_goal).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(frame_display, text="Mark as Complete", command=self.mark_goal_complete).grid(row=3, column=0, padx=5, pady=5, sticky="ew")


        ttk.Button(frame_display, text="Visualize Goal Progress", command=self.visualize_goal_progress).grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(frame_display, text="Visualize Goal Forecast", command=self.visualize_goal_forecasts).grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(frame_display, text="Goal Gauge", command=self.visualize_goal_gauge).grid(row=6, column=0, padx=5, pady=5, sticky= 'ew')

    def add_goal(self):
        try:
            goal = self.goal_entry.get()
            target_amount = Decimal(self.target_amount_entry.get())
            due_date = self.due_date_entry.get_date()
            initial_deposit = Decimal(self.initial_deposit_entry.get())
            from_payment_method = self.payment_method_combobox.get()

            self.account_manager.add_payment_method(goal, "cash", initial_balance=initial_deposit)
            if initial_deposit > 0:
                self.account_manager.update_balance(from_payment_method, initial_deposit, "Expense")

            self.goal_manager.add_goal(goal, target_amount, due_date, initial_deposit)

            messagebox.showinfo("Success", f"Goal '{goal}' added successfully with an initial deposit of {initial_deposit} from {from_payment_method}.")
            self.update_goals_tree()
            self.refresh_ui_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_money_to_goal(self):
        try:
            goal_id = int(self.goal_id_entry.get())
            amount_to_add = Decimal(self.amount_entry.get())
            from_payment_method = self.add_payment_method_combobox.get()

            if amount_to_add > 0:
                self.account_manager.update_balance(from_payment_method, amount_to_add, "Expense")
                goal_name = self.goal_manager.get_goal_name(goal_id)
                self.account_manager.update_balance(goal_name, amount_to_add, "Income")
                self.goal_manager.update_goal(goal_id, amount_to_add)

                messagebox.showinfo("Success", f"Added {amount_to_add} to goal '{goal_name}' from {from_payment_method}.")
                self.update_goals_tree()
                self.refresh_ui_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_goal(self):
        try:
            selected_item = self.goals_tree.selection()[0]
            goal_id = self.goals_tree.item(selected_item, 'values')[0]
            goal_name = self.goals_tree.item(selected_item, 'values')[1]
            goal_balance = self.goal_manager.get_goal_balance(goal_id)

            # Remove the payment method associated with the goal
            self.account_manager.remove_payment_method(goal_name)

            # Transfer the balance back to cash
            if goal_balance > 0:
                self.account_manager.update_balance("cash", goal_balance, "Income")

            # Remove the goal
            self.goal_manager.delete_goal(goal_id)

            messagebox.showinfo("Success", f"Goal '{goal_name}' deleted. {goal_balance} has been transferred to cash.")
            self.update_goals_tree()
            self.refresh_ui_callback()
        except IndexError:
            messagebox.showerror("Error", "No goal selected")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mark_goal_complete(self):
        try:
            selected_item = self.goals_tree.selection()[0]
            goal_id = self.goals_tree.item(selected_item, 'values')[0]
            self.goal_manager.mark_goal_complete(goal_id)
            self.update_goals_tree()
        except IndexError:
            messagebox.showerror("Error", "No goal selected")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_goals_tree(self):
        for item in self.goals_tree.get_children():
            self.goals_tree.delete(item)
        
        goals_df = self.goal_manager.get_goals()
        
        for _, row in goals_df.iterrows():
            completed_text = "Yes" if row['Completed'] else "No"
            self.goals_tree.insert(
                "", "end", 
                values=(row['ID'], row['Goal'], row['Target Amount'], row['Current Amount'], row['Due Date'], completed_text)
            )

    def visualize_goal_progress(self):
        goal_progress = self.goal_manager.calculate_goal_progress()
        goal_progress.plot(kind='bar', x='Goal', y='Progress', color='blue', figsize=(10, 5))
        plt.title('Goal Progress')
        plt.xlabel('Goals')
        plt.ylabel('Progress (%)')
        plt.show()

    def visualize_goal_forecasts(self):
        goal_forecasts = self.goal_manager.forecast_goal_completion()
        goal_forecasts.plot(kind='bar', x='Goal', y='Days to Complete', color='orange', figsize=(10, 5))
        plt.title('Goal Completion Forecast')
        plt.xlabel('Goals')
        plt.ylabel('Days to Complete')
        plt.show()

    def visualize_goal_gauge(self):
        try:
            goals_df = self.goal_manager.get_goals()
            for _, row in goals_df.iterrows():
                self.goal_manager.visualize_goal_gauge(row['Goal'], row['Target Amount'], row['Current Amount'])
        except Exception as e:
            messagebox.showerror("Error", str(e))