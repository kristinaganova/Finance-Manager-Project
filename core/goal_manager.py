import pandas as pd
from decimal import Decimal
import sqlite3
from utils.initialize_database import DATABASE_PATH

class GoalManager:
    def __init__(self, conn, user):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.user = user
        self.goals = self.load_goals()

    def load_goals(self):
        self.cursor.execute('''
            SELECT id, goal, target_amount, current_amount, due_date, completed
            FROM goals
            WHERE user_id = ?
        ''', (self.user.user_id,))
        goals = self.cursor.fetchall()

        goals_df = pd.DataFrame(goals, columns=['ID', 'Goal', 'Target Amount', 'Current Amount', 'Due Date', 'Completed'])
        return goals_df

    def set_user(self, user):
        self.user = user
        self.goals = self.load_goals()  # Reload goals for the new user

    def add_goal(self, goal, target_amount, due_date):
        if not isinstance(target_amount, Decimal):
            target_amount = Decimal(str(target_amount))
        self._store_goal_in_db(goal, target_amount, due_date)
        self.goals = self.load_goals()  # Reload goals after adding

    def mark_goal_complete(self, goal_id):
        self._update_goal_status(goal_id, completed=True)
        self.goals = self.load_goals()  # Reload goals after update

    def delete_goal(self, goal_id):
        self._remove_goal_from_db(goal_id)
        self.goals = self.load_goals()  # Reload goals after deletion

    def update_goal(self, goal_id, amount):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        if goal_id not in self.goals['ID'].values:
            raise ValueError("Goal not found.")
        self._update_goal_amount_in_db(goal_id, amount)
        self.goals = self.load_goals()  # Reload goals after update

    def get_goals(self):
        return self.goals

    def calculate_goal_progress(self):
        self.goals['Progress'] = self.goals.apply(lambda row: round((row['Current Amount'] / row['Target Amount']) * 100, 2), axis=1)
        return self.goals

    def forecast_goal_completion(self, days_ahead=30):
        self.goals['Days to Complete'] = self.goals.apply(
            lambda row: (row['Target Amount'] - row['Current Amount']) / (row['Current Amount'] / days_ahead)
            if row['Current Amount'] > 0 else None, axis=1)
        return self.goals

    def _store_goal_in_db(self, goal, target_amount, due_date):
        self.cursor.execute('''
            INSERT INTO goals (user_id, goal, target_amount, current_amount, due_date, completed)
            VALUES (?, ?, ?, ?, ?, 0)
        ''', (self.user.user_id, goal, float(target_amount), 0, due_date))
        self.conn.commit()

    def _update_goal_amount_in_db(self, goal_id, amount):
        self.cursor.execute('''
            UPDATE goals SET current_amount = current_amount + ? WHERE id = ? AND user_id = ?
        ''', (float(amount), goal_id, self.user.user_id))
        self.conn.commit()

    def _update_goal_status(self, goal_id, completed):
        self.cursor.execute('''
            UPDATE goals SET completed = ? WHERE id = ? AND user_id = ?
        ''', (1 if completed else 0, goal_id, self.user.user_id))
        self.conn.commit()

    def _remove_goal_from_db(self, goal_id):
        self.cursor.execute('''
            DELETE FROM goals WHERE id = ? AND user_id = ?
        ''', (goal_id, self.user.user_id))
        self.conn.commit()
