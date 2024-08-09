import sqlite3

def display_data():
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()
    
    # Display users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("Users:")
    for user in users:
        print(user)
    
    # Display payment_methods
    cursor.execute("SELECT * FROM payment_methods")
    payment_methods = cursor.fetchall()
    print("\nPayment Methods:")
    for method in payment_methods:
        print(method)
    
    # Display transactions
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    print("\nTransactions:")
    for transaction in transactions:
        print(transaction)
    
    # Display goals
    cursor.execute("SELECT * FROM goals")
    goals = cursor.fetchall()
    print("\nGoals:")
    for goal in goals:
        print(goal)
    
    
    
    conn.close()

if __name__ == "__main__":
    display_data()
