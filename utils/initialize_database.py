import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'finance_manager.db')

def initialize_database(db_name='finance_manager.db'):
    conn = sqlite3.connect(db_name)
    
    # Enable foreign key constraint
    conn.execute('PRAGMA foreign_keys = ON;')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            method_name TEXT NOT NULL,
            method_type TEXT NOT NULL,
            balance REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,  -- Could use DATE or DATETIME type
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            payment_method_id INTEGER NOT NULL,
            currency TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (payment_method_id) REFERENCES payment_methods (id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_amount REAL NOT NULL,
            due_date TEXT NOT NULL,  -- Could use DATE or DATETIME type
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

def add_completed_column(db_name='finance_manager.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        ALTER TABLE goals ADD COLUMN completed BOOLEAN NOT NULL DEFAULT 0
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    add_completed_column()
