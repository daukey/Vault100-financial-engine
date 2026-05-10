import operations
import os
from datetime import datetime

def export_to_text(file_name=None, start_date=None, end_date=None):
    """
    Exports transactions to a text file.
    Supports optional date range filtering.
    """
    if not file_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = "statement_{}.txt".format(timestamp)

    history = operations.get_transaction_history(start_date, end_date)
    file_path = os.path.join("exports", file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Vault100 - Financial Statement\n")
            f.write("==============================\n")

            if start_date and end_date:
                f.write("Period: {} to {}\n".format(start_date, end_date))

            f.write("Generated: {}\n\n".format(
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))

            f.write("{:<18} | {:<10} | {:<12} | {:<15} | {:<20}\n".format(
                "Date", "Type", "Amount (TL)", "Category", "Description"
            ))
            f.write("-" * 80 + "\n")

            for item in history:
                f.write("{:<18} | {:<10} | {:<12.2f} | {:<15} | {:<20}\n".format(
                    item["date"],
                    item["type"],
                    item["amount"],
                    item["category"] or "-",
                    item["description"] or "-",
                ))

            balance = operations.calculate_current_balance()
            f.write("\n" + "=" * 80 + "\n")
            f.write("NET BALANCE: {:.2f} TL\n".format(balance))

        print("System: Export saved at: {}".format(file_path))
        return file_path  # FIX: return path so UI can show the filename
    except Exception as e:
        print("System: Export failed. Error: {}".format(e))
        return None