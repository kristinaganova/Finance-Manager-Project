import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizer:
    def __init__(self):
        pass

    def visualize_statistics(self, stats):
        categories = list(stats.keys())
        values = list(stats.values())
        
        plt.figure(figsize=(10, 5))
        plt.bar(categories, values, color='skyblue')
        plt.title('Transaction Statistics')
        plt.xlabel('Statistics')
        plt.ylabel('Value')
        plt.xticks(rotation=45)
        plt.show()

    def visualize_correlations(self, correlations):
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlations, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')
        plt.show()

    def visualize_forecast(self, future_expenses, future_income):
        dates = pd.date_range(start=pd.Timestamp.now(), periods=len(future_expenses), freq='D')
        
        plt.figure(figsize=(10, 5))
        plt.plot(dates, future_expenses, label='Forecasted Expenses', color='red')
        plt.plot(dates, future_income, label='Forecasted Income', color='green')
        plt.title('Income and Expenses Forecast')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.legend()
        plt.show()

    def visualize_goal_progress(self, goal_progress):
        goal_progress = pd.DataFrame(goal_progress)
        goal_progress.plot(kind='bar', x='Goal', y='Progress', color='blue', figsize=(10, 5))
        plt.title('Goal Progress')
        plt.xlabel('Goals')
        plt.ylabel('Progress (%)')
        plt.show()

    def visualize_goal_forecasts(self, goal_forecasts):
        goal_forecasts = pd.DataFrame(goal_forecasts)
        goal_forecasts.plot(kind='bar', x='Goal', y='Days to Complete', color='orange', figsize=(10, 5))
        plt.title('Goal Completion Forecast')
        plt.xlabel('Goals')
        plt.ylabel('Days to Complete')
        plt.show()
