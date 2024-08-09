import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import pandas as pd

class Visualizer:
    def __init__(self, transactions):
        self.transactions = transactions

    def visualize_data(self):
        self.transactions['Date'] = pd.to_datetime(self.transactions['Date'])

        fig, ax = plt.subplots()
        for category in self.transactions['Category'].unique():
            category_data = self.transactions[self.transactions['Category'] == category]
            ax.plot(category_data['Date'], category_data['Amount'], label=category)

        ax.set_xlabel('Date')
        ax.set_ylabel('Amount')
        ax.set_title('Expenses by Category Over Time')
        ax.legend()
        plt.show()

    def visualize_forecast(self, future_expenses, future_income):
        future_dates = [datetime.now() + timedelta(days=i) for i in range(1, len(future_expenses) + 1)]

        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Scatter(x=future_dates, y=future_expenses, mode='lines', name='Future Expenses'))
        fig.add_trace(go.Scatter(x=future_dates, y=future_income, mode='lines', name='Future Income'))

        fig.update_layout(title='Forecast of Future Expenses and Income',
                          xaxis_title='Date',
                          yaxis_title='Amount')
        fig.show()