import sqlite3
import bcrypt

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    @staticmethod
    def register_user(username, password):
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) if password else b''
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (username, hashed_password))
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
            SELECT id, username, password FROM users
            WHERE username = ?
        ''', (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            stored_password = user[2]
            if not stored_password: 
                return User(user[0], user[1])
            elif bcrypt.checkpw(password.encode('utf-8'), stored_password):
                return User(user[0], user[1])
        return None
