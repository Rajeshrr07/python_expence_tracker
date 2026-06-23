document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const displayBudget = document.getElementById('display-budget');
    const displayTotal = document.getElementById('display-total');
    const displayRemaining = document.getElementById('display-remaining');
    const budgetWarning = document.getElementById('budget-warning');
    const expensesBody = document.getElementById('expenses-body');
    
    const budgetForm = document.getElementById('budget-form');
    const budgetInput = document.getElementById('budget-input');
    
    const expenseForm = document.getElementById('expense-form');
    const dateInput = document.getElementById('date');
    const categorySelect = document.getElementById('category');
    const amountInput = document.getElementById('amount');
    const descriptionInput = document.getElementById('description');

    // State
    let budget = 0;
    let expenses = [];

    // Format currency
    const formatMoney = (amount) => {
        return '₹' + parseFloat(amount).toFixed(2);
    };

    // Calculate and update UI stats
    const updateStats = () => {
        const total = expenses.reduce((sum, exp) => sum + parseFloat(exp.amount), 0);
        const remaining = budget - total;

        displayBudget.textContent = formatMoney(budget);
        displayTotal.textContent = formatMoney(total);
        displayRemaining.textContent = formatMoney(remaining);

        if (total > budget && budget > 0) {
            budgetWarning.classList.remove('hidden');
            displayRemaining.style.color = 'var(--danger)';
        } else {
            budgetWarning.classList.add('hidden');
            displayRemaining.style.color = 'inherit';
        }
    };

    // Render table
    const renderTable = () => {
        expensesBody.innerHTML = '';
        // sort by date descending
        const sorted = [...expenses].sort((a, b) => new Date(b.date) - new Date(a.date));
        
        sorted.forEach(exp => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${exp.date}</td>
                <td><span style="background: rgba(255,255,255,0.1); padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">${exp.category}</span></td>
                <td>${exp.description}</td>
                <td style="font-weight: 600;">${formatMoney(exp.amount)}</td>
            `;
            expensesBody.appendChild(tr);
        });
    };

    // Fetch initial data
    const loadData = async () => {
        try {
            const budgetRes = await fetch('/api/budget');
            const budgetData = await budgetRes.json();
            budget = budgetData.budget;

            const expRes = await fetch('/api/expenses');
            expenses = await expRes.json();

            updateStats();
            renderTable();
        } catch (error) {
            console.error("Error loading data:", error);
        }
    };

    // Handle Budget Submit
    budgetForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const newBudget = parseFloat(budgetInput.value);
        if (isNaN(newBudget) || newBudget < 0) return;

        try {
            const res = await fetch('/api/budget', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ budget: newBudget })
            });
            if (res.ok) {
                budget = newBudget;
                budgetInput.value = '';
                updateStats();
            }
        } catch (error) {
            console.error("Error updating budget:", error);
        }
    });

    // Handle Expense Submit
    expenseForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const expense = {
            date: dateInput.value,
            category: categorySelect.value,
            amount: parseFloat(amountInput.value),
            description: descriptionInput.value
        };

        try {
            const res = await fetch('/api/expenses', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(expense)
            });
            
            if (res.ok) {
                expenses.push(expense);
                expenseForm.reset();
                dateInput.valueAsDate = new Date(); // Reset date to today
                updateStats();
                renderTable();
            }
        } catch (error) {
            console.error("Error adding expense:", error);
        }
    });

    // Initialize date input to today
    dateInput.valueAsDate = new Date();
    
    // Initial load
    loadData();
});
