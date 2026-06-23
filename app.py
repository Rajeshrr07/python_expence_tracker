from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)

CSV_FILE = 'expenses.csv'
BUDGET_FILE = 'budget.txt'

def read_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, 'r') as f:
            try:
                return float(f.read().strip())
            except ValueError:
                return 0.0
    return 0.0

def write_budget(amount):
    with open(BUDGET_FILE, 'w') as f:
        f.write(str(amount))

def get_expenses():
    expenses = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row['amount'] = float(row['amount'])
                except ValueError:
                    row['amount'] = 0.0
                expenses.append(row)
    return expenses

def save_expense(expense):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['date', 'category', 'amount', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(expense)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET', 'POST'])
def handle_expenses():
    if request.method == 'POST':
        data = request.json
        if not all(k in data for k in ('date', 'category', 'amount', 'description')):
            return jsonify({'error': 'Missing fields'}), 400
            
        try:
            data['amount'] = float(data['amount'])
        except ValueError:
            return jsonify({'error': 'Invalid amount'}), 400

        save_expense({
            'date': data['date'],
            'category': data['category'],
            'amount': data['amount'],
            'description': data['description']
        })
        return jsonify({'message': 'Expense saved successfully'}), 201
    
    return jsonify(get_expenses())

@app.route('/api/budget', methods=['GET', 'POST'])
def handle_budget():
    if request.method == 'POST':
        data = request.json
        if 'budget' not in data:
            return jsonify({'error': 'Missing budget field'}), 400
        try:
            budget = float(data['budget'])
            write_budget(budget)
            return jsonify({'message': 'Budget updated successfully'}), 200
        except ValueError:
            return jsonify({'error': 'Invalid budget amount'}), 400

    return jsonify({'budget': read_budget()})

if __name__ == '__main__':
    app.run(debug=True)
