import database
from datetime import datetime

def add_transaction(amount, category, transaction_type, description, username):
    conn = database.get_connection()
    cursor = conn.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d- %H:%M")

    record = (
        float(amount),
        category or "General",
        transaction_type,
        current_date,
        description,
        username
    )

    try:
        cursor.execute("""
            INSERT INTO transactions (amount, category, type, date, description, added_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, record)
        conn.commit()
        print("System: Added {} of {}.".format(transaction_type, amount))
        return True
    except Exception as e:
        print("System: Error adding transaction: {}".format(e))
        return False
    finally:
        conn.close()

def get_transaction_history(start_date=None, end_date=None):
    """
    Returns all transactions as a list of dicts.
    Optionally filter by date range (strings: "YYYY-MM-DD").
    """
    conn = database.get_connection()
    cursor = conn.cursor()

    if start_date and end_date:
        cursor.execute("""
            SELECT id, amount, category, type, date, description, added_by
            FROM transactions
            WHERE date >= ? AND date <= ?
            ORDER BY date DESC
        """, (start_date, end_date + " 23:59"))
    else:
        cursor.execute("""
            SELECT id, amount, category, type, date, description, added_by
            FROM transactions
            ORDER BY date DESC
        """)

    history = []
    for row in cursor.fetchall():
        history.append({
            "id": row["id"],
            "amount": row["amount"],
            "category": row["category"],
            "type": row["type"],
            "date": row["date"],
            "description": row["description"],
            "added_by": row["added_by"],
        })

    conn.close()
    return history

def delete_transaction(transaction_id):
    database.delete_transaction(transaction_id)
    print("System: Transaction {} deleted.".format(transaction_id))

def calculate_current_balance():
    history = get_transaction_history()
    balance = 0.0
    for item in history:
        if item["type"] == "Income":
            balance += item["amount"]
        elif item["type"] == "Expense":
            balance -= item["amount"]
    print("System: Current balance: {:.2f}".format(balance))
    return balance