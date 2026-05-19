import operations
import os
from datetime import datetime

def export_to_text(file_name=None, username=None, start_date=None, end_date=None):
    if not file_name:
        timestamp=datetime.now().strftime("%d%m%Y_%H%M%S")
        file_name="export_{}.txt".format(timestamp)

    history=operations.get_transaction_history(
        username=username,
        start_date=start_date,
        end_date=end_date
    )
    file_path=os.path.join("exports", file_name)
    try:
        with open(file_path,"w") as f:
            f.write("Vault100 - Financial Export\n")
            f.write("==============================\n")
            if username:
                f.write("User: {}\n".format(username))
            if start_date and end_date:
                f.write("Period: {} to {}\n".format(start_date, end_date))
            f.write("Generated: {}\n\n".format(
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))
            f.write("{:<18}|{:<10}|{:<12}|{:<15}|{:<20}\n".format(
                "Date","Type","Amount(TL)","Category","Description"
            ))
            f.write("-"*80+"\n")
            for item in history:
                f.write("{:<18}|{:<10}|{:<12.2f}|{:<15}|{:<20}\n".format(
                    item["date"],
                    item["type"],
                    item["amount"],
                    item["category"] or "-",
                    item["description"] or "-",
                ))
            balance=operations.calculate_current_balance(username=username)
            f.write("\n"+"="*80+"\n")
            f.write("NET BALANCE: {:.2f} TL\n".format(balance))

        print("Export saved at: {}".format(file_path))
        return file_path
    except Exception as e:
        print("Export failed. Error: {}".format(e))
        return None