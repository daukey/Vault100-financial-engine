import sqlite3
import database

def verify_user(username, password):
    if not username or not password:
        return None

    conn=database.get_users_connection()
    cursor=conn.cursor()
    cursor.execute(
        "SELECT username, role FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    result=cursor.fetchone()
    conn.close()

    if result:
        print("Login OK — {} ({})".format(result["username"], result["role"])) #test
        return {
            "username":result["username"],
            "role":result["role"],
            "is_authenticated":True
        }

    print("Login failed for '{}'.".format(username)) #why
    return None

def username_exists(username):
    conn=database.get_users_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result=cursor.fetchone()
    conn.close()
    return result is not None

def register_user(username,password):
    if not username or not password:
        return False,"Username and password cannot be empty."
    if len(username)<3:
        return False,"Username must be at least 3 characters."
    if len(password)<4:
        return False,"Password must be at least 4 characters."
    if username_exists(username):
        return False,"Username already taken."
    success=database.add_user(username, password, role="user")
    if success:
        return True,"Account created! Redirecting to login..."
    return False,"Registration failed. Try again."

def get_all_users():
    return database.get_all_users()

def add_user(username, password,role="user"):
    return database.add_user(username,password,role)

def delete_user(username):
    database.delete_user(username)