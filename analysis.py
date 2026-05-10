import operations

def get_category_totals(start_date=None, end_date=None):
    history = operations.get_transaction_history(start_date, end_date)
    summary = {}
    for item in history:
        if item["type"] == "Expense":
            cat = item["category"] or "General"
            summary[cat] = summary.get(cat, 0) + item["amount"]
    print("System: Category analysis done for {} items.".format(len(history)))
    return summary

def get_income_vs_expense(start_date=None, end_date=None):
    history = operations.get_transaction_history(start_date, end_date)
    totals = {"Income": 0.0, "Expense": 0.0}
    for item in history:
        if item["type"] == "Income":
            totals["Income"] += item["amount"]
        else:
            totals["Expense"] += item["amount"]
    return totals