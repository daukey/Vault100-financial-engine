import database

def verify_user(username, password):
    if not username or not password:
        return None

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, role FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        print("System: Login successful for {} as {}.".format(result["username"], result["role"]))
        return {
            "username": result["username"],
            "role": result["role"],
            "is_authenticated": True
        }

    print("System: Login failed for user: {}".format(username))
    return None

def get_all_users():
    return database.get_all_users()

def add_user(username, password, role="user"):
    return database.add_user(username, password, role)

def delete_user(username):
    database.delete_user(username)