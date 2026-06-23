import csv
import os

# Global list to store expenses
expenses = []
CSV_FILE = 'expenses.csv'

def add_expense():
    """Prompts user for expense details and adds it to the list."""
    date = input("Enter the date of the expense (YYYY-MM-DD): ").strip()
    category = input("Enter the category of the expense (e.g., Food, Travel): ").strip()
    amount_str = input("Enter the amount spent: ").strip()
    description = input("Enter a brief description of the expense: ").strip()

    try:
        amount = float(amount_str)
    except ValueError:
        print("Invalid amount entered. Please try again.")
        return

    expense = {
        'date': date,
        'category': category,
        'amount': amount,
        'description': description
    }
    expenses.append(expense)
    print("Expense added successfully!")

def view_expenses():
    """Retrieves and displays all stored expenses with validation."""
    if not expenses:
        print("No expenses to show.")
        return

    print("\n--- All Expenses ---")
    for expense in expenses:
        date = expense.get('date', '').strip()
        category = expense.get('category', '').strip()
        amount = expense.get('amount')
        description = expense.get('description', '').strip()

        # Validate the data before displaying it
        if not date or not category or amount is None or not description:
            print("Incomplete entry found and skipped.")
            continue

        print(f"Date: {date} | Category: {category} | Amount: {amount} | Description: {description}")
    print("--------------------")

def input_budget():
    """Allows the user to input a monthly budget."""
    budget_str = input("Enter the total amount you want to budget for the month: ").strip()
    try:
        return float(budget_str)
    except ValueError:
        print("Invalid input. Using 0.0 as budget.")
        return 0.0

def calculate_total_expenses():
    """Calculates the total expenses recorded so far."""
    total = 0.0
    for exp in expenses:
        try:
            total += float(exp.get('amount', 0))
        except (ValueError, TypeError):
            pass
    return total

def track_budget():
    """Tracks expenses against the user-defined monthly budget."""
    budget = input_budget()
    total_expenses = calculate_total_expenses()
    
    if total_expenses > budget:
        print("You have exceeded your budget!")
    else:
        remaining = budget - total_expenses
        print(f"You have {remaining:.2f} left for the month.")

def save_expenses():
    """Saves all expenses to a CSV file."""
    try:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['date', 'category', 'amount', 'description']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(expenses)
        print("Expenses saved successfully!")
    except Exception as e:
        print(f"Failed to save expenses: {e}")

def load_expenses():
    """Loads expenses from the CSV file."""
    global expenses
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert amount back to float when loading
                    try:
                        row['amount'] = float(row['amount'])
                    except ValueError:
                        pass
                    expenses.append(row)
            print("Loaded previous expenses.")
        except Exception as e:
            print(f"Failed to load expenses: {e}")
    else:
        print("No existing expense file found. Starting fresh.")

def main_menu():
    """Displays the interactive menu and handles choices."""
    load_expenses()
    
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Track budget")
        print("4. Save expenses")
        print("5. Exit")
        
        choice = input("Enter a number to choose an option: ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            track_budget()
        elif choice == '4':
            save_expenses()
        elif choice == '5':
            save_expenses()
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()
