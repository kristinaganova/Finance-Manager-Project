import sqlite3

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    @staticmethod
    def register_user(username, password):
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (username, password))
            conn.commit()
            return User(cursor.lastrowid, username)
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @staticmethod
    def login_user(username, password):
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username FROM users
            WHERE username = ? AND password = ?
        ''', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(user[0], user[1])
        return None
