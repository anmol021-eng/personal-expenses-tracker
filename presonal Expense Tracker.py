import os
import csv
from datetime import datetime
try:
    import pandas as pd
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd

FILE = "expenses.csv"
COLUMNS = ["Date", "Category", "Description", "Amount"]


# create the csv file with header if it doesn't exist
def setup_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            csv.writer(f).writerow(COLUMNS)


def count_records():
    return len(pd.read_csv(FILE))


def show_num(n):
    # show 250.0 as 250 and 250.5 as 250.5
    return int(n) if float(n) == int(n) else round(float(n), 2)


def add_expense():
    date = input("Enter date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use format YYYY-MM-DD. Expense not saved.")
        return

    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()
    if category == "":
        print("Category cannot be empty. Expense not saved.")
        return

    amount_text = input("Enter amount: ").strip()
    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Invalid amount. Amount must be a positive number. Expense not saved.")
        return

    with open(FILE, "a", newline="") as f:
        csv.writer(f).writerow([date, category, description, amount])

    print("Expense saved. Total records:", count_records())


def category_summary():
    df = pd.read_csv(FILE)
    if df.empty:
        print("No expenses yet.")
        return

    totals = df.groupby("Category")["Amount"].sum()
    parts = [f"{cat}: {show_num(amt)}" for cat, amt in totals.items()]
    print(" | ".join(parts))
    print("Total:", show_num(df["Amount"].sum()))


def monthly_summary():
    df = pd.read_csv(FILE)
    if df.empty:
        print("No expenses yet.")
        return

    df["Month"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m")
    totals = df.groupby("Month")["Amount"].sum()
    for month, amt in totals.items():
        print(f"{month}: {show_num(amt)}")
    print("Total:", show_num(df["Amount"].sum()))


def main():
    setup_file()
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add expense")
        print("2. Monthly summary")
        print("3. Category summary")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            monthly_summary()
        elif choice == "3":
            category_summary()
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Wrong choice, try again.")


main()