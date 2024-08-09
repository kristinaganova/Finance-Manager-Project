import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans
from plotly import graph_objects as go

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

    def visualize_distribution(self, transactions, title, column):
        plt.figure(figsize=(10, 5))
        sns.histplot(transactions[column], kde=True, color='blue', bins=30)
        plt.title(f'Distribution of {title}')
        plt.xlabel('Amount')
        plt.ylabel('Frequency')
        plt.show() 

    def visualize_time_series(self, transactions):
        transactions['Date'] = pd.to_datetime(transactions['Date'])
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='Date', y='Amount', hue='Type', data=transactions)
        plt.title('Time Series of Transactions')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.xticks(rotation=45)
        plt.show()

    def visualize_category_comparison(self, transactions):
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='Category', y='Amount', data=transactions[transactions['Type'] == 'Expense'])
        plt.title('Expense Distribution by Category')
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.xticks(rotation=45)
        plt.show()

    def visualize_extended_correlations(self, transactions, balances):
        data = transactions.pivot_table(values='Amount', index='Date', columns='Type', aggfunc='sum').fillna(0)
        balance_df = pd.DataFrame(list(balances.items()), columns=['Payment Method', 'Balance'])
        combined = pd.concat([data, balance_df], axis=1)
        
        correlations = combined.corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlations, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Extended Correlation Matrix')
        plt.show()

    def visualize_goal_gauge(self, goal, target_amount, current_amount):
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_amount,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': goal},
            delta={'reference': target_amount},
            gauge={'axis': {'range': [None, target_amount]},
                   'bar': {'color': "darkblue"},
                   'steps': [{'range': [0, target_amount * 0.5], 'color': "lightgray"},
                             {'range': [target_amount * 0.5, target_amount], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': target_amount}}))
        fig.show()

    def visualize_clusters(self, transactions):
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