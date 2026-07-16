import csv
import os
from datetime import datetime

# --- PATH LOCKING ---
# Ensures expenses.csv stays exactly inside the script's folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(SCRIPT_DIR, "expenses.csv")


def initialize_csv():
    """Creates the CSV file with headers if it doesn't exist yet."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Define columns for our spreadsheet
            writer.writerow(["Category", "Amount", "Description", "Date"])


def add_expense():
    """Logs a new expense row into the CSV file."""
    print("\n--- Log New Expense ---")
    print("Categories: Food, Transport, Bills, Entertainment, Other")
    category = input("Enter category: ").strip().capitalize()
    
    if not category:
        category = "Other"

    # Validate amount using a try-except block
    while True:
        try:
            amount = float(input("Enter amount ($): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("❌ Invalid input! Please enter a valid number (e.g., 12.50).")

    description = input("Enter description/notes: ").strip()
    if not description:
        description = "N/A"

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Open CSV in "a" (append) mode to write a single new row
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([category, amount, description, date_str])
        
    print(f"💰 Saved: ${amount:.2f} spent on {category}!")


def view_summary():
    """Reads the CSV file, calculates category totals, and prints a summary."""
    print("\n--- EXPENSE REPORT SUMMARY ---")
    
    if not os.path.exists(CSV_FILE):
        print("No expenses recorded yet.")
        return

    total_spending = 0.0
    category_totals = {}

    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader) # Skip the header row ["Category", "Amount", ...]

        print(f"\n%-15s %-10s %-20s %-15s" % (header[0], header[1], header[2], header[3]))
        print("-" * 65)

        for row in reader:
            # Extract values matching our columns
            category = row[0]
            amount = float(row[1]) # Convert string back to float for math
            description = row[2]
            date = row[3]

            print("%-15s $%-9.2f %-20s %-15s" % (category, amount, description, date))

            # Accumulate metrics
            total_spending += amount
            category_totals[category] = category_totals.get(category, 0.0) + amount

    print("-" * 65)
    print(f"💵 TOTAL WALLET OUTFLOW: ${total_spending:.2f}")
    
    print("\n📊 SPENDING BY CATEGORY:")
    for cat, total in category_totals.items():
        percentage = (total / total_spending) * 100
        print(f" * {cat}: ${total:.2f} ({percentage:.1f}%)")


def main():
    initialize_csv()
    while True:
        print("\n=== PERSONAL EXPENSE TRACKER ===")
        print("1. Log an Expense")
        print("2. View Expense Summary & Analytics")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_summary()
        elif choice == "3":
            print("Closing tracker. Check out 'expenses.csv' to view it in Excel!")
            break
        else:
            print("Invalid selection. Try again.")


if __name__ == "__main__":
    main()