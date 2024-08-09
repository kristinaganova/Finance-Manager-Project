import pandas as pd
from decimal import Decimal

class GoalManager:
    def __init__(self):
        self.goals = pd.DataFrame(columns=['Goal', 'Target Amount', 'Current Amount', 'Due Date'])

    def add_goal(self, goal, target_amount, due_date):
        if not isinstance(target_amount, Decimal):
            target_amount = Decimal(str(target_amount))
        new_goal = pd.DataFrame({
            'Goal': [goal], 
            'Target Amount': [target_amount], 
            'Current Amount': [Decimal(0)], 
            'Due Date': [due_date]
        })
        self.goals = pd.concat([self.goals, new_goal], ignore_index=True)

    def update_goal(self, index, amount):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        if index in self.goals.index:
            self.goals.at[index, 'Current Amount'] += amount
        else:
            print("Goal not found.")

    def get_goals(self):
        return self.goals