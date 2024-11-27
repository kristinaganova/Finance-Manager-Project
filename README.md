# Finance Manager Project

Finance Manager is a desktop application designed to help users manage their personal finances. It provides tools for tracking transactions, managing savings goals, and organizing payment methods such as bank cards and cash. The app also offers visualizations and reports to help users understand their financial habits and plan for the future.

---

## Features

### User Management
- **Registration**: Allows new users to create accounts with a username and password.
- **Login**: Existing users can securely log in to their accounts.
- **User Data**: Each user has their own transactions, goals, and payment methods, securely stored and accessible only to them.

### Transaction Management
- **Add Transactions**: Users can add transactions by specifying the date, category, amount, type (income or expense), payment method, and currency.
- **Delete Transactions**: Users can delete existing transactions, which automatically updates the balance of the associated payment method.
- **Transaction Visualization**: Users can view all transactions in a table format and generate visualizations such as spending distribution charts and time series.

### Payment Method Management
- **Add Payment Methods**: Users can add new payment methods (e.g., new cards or cash) by specifying a name, type, and starting balance.
- **Delete Payment Methods**: Users can delete payment methods. Any associated goals are updated accordingly.
- **Balance Tracking**: Users can track the current balances of all payment methods.

### Financial Goal Management
- **Add Goals**: Users can set financial goals with a name, target amount, deadline, and initial deposit.
- **Add Funds to Goals**: Users can allocate funds to goals from specific payment methods.
- **Delete Goals**: Users can delete goals and transfer the balance back to the payment method.
- **Progress Tracking**: Users can track goal progress through visualizations such as graphs and progress indicators.

### Visualizations and Reports
- **Statistical Reports**: Generate reports including averages, medians, and standard deviations for transactions.
- **Correlations**: Analyze correlations between spending categories.
- **Forecasting**: Predict future income and expenses based on historical data.
- **Clustering**: Identify trends through clustering analysis.

---

## Technologies Used
- **Programming Language**: Python  
- **GUI**: Tkinter  
- **Database**: SQLite  
- **Visualization Libraries**: Matplotlib, Seaborn, Plotly  
- **Password Encryption**: bcrypt  
