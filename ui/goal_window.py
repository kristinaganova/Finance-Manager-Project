import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from decimal import Decimal

class GoalWindow:
    def __init__(self, root, finance_manager):
        self.root = root
        self.root.title("Manage Goals")
        self.goal_manager = finance_manager.goal_manager

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

    def add_goal(self):
        try:
            goal = self.goal_entry.get()
            target_amount = Decimal(self.target_amount_entry.get())
            due_date = self.due_date_entry.get_date()
            self.goal_manager.add_goal(goal, target_amount, due_date)
            self.update_goals_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_goal(self):
        try:
            selected_item = self.goals_tree.selection()[0]
            goal_id = self.goals_tree.item(selected_item, 'values')[0]  # Assuming the first column is the goal ID
            self.goal_manager.delete_goal(goal_id)
            self.update_goals_tree()  # Refresh the tree after deletion
        except IndexError:
            messagebox.showerror("Error", "No goal selected")
            
    def mark_goal_complete(self):
        try:
            selected_item = self.goals_tree.selection()[0]
            goal_id = self.goals_tree.item(selected_item, 'values')[0]
            self.goal_manager.mark_goal_complete(goal_id)
            self.update_goals_tree()  # Refresh the tree after marking complete
        except IndexError:
            messagebox.showerror("Error", "No goal selected")

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
