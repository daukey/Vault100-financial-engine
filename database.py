import sqlite3
import os

def prepare_directories():
    folders = ["data", "exports"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print("System: Created '{}' directory.".format(folder))

def get_connection():
    conn = sqlite3.connect("data/vault100.db")
    conn.row_factory = sqlite3.Row  # FIX: lets us access columns by name
    return conn

def initialize_database():
    prepare_directories()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            type TEXT,
            date TEXT,
            description TEXT,
            added_by TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ('admin', '1234', 'admin'))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ('user', '5678', 'user'))

    default_cats = [('Food',), ('Rent',), ('Salary',), ('Bills',), ('Fun',)]
    cursor.executemany("INSERT OR IGNORE INTO categories (name) VALUES (?)", default_cats)

    conn.commit()
    conn.close()
    print("System: Database initialized successfully.")

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = [{"id": row["id"], "username": row["username"], "role": row["role"]}
             for row in cursor.fetchall()]
    conn.close()
    return users

def add_user(username, password, role="user"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        conn.commit()
        print("System: User '{}' added.".format(username))
        return True
    except sqlite3.IntegrityError:
        print("System: Username '{}' already exists.".format(username))
        return False
    finally:
        conn.close()

def delete_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ? AND role != 'admin'", (username,))
    conn.commit()
    conn.close()

def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()