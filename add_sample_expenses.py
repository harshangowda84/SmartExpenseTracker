#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta
import random

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
django.setup()

from expenses.models import Expense, Category
from django.contrib.auth.models import User

try:
    admin_user = User.objects.get(username='admin')
    
    # Sample expense data for the last 30 days
    expense_data = [
        # Week 1 (July 17-23, 2025)
        {'amount': 450, 'description': 'Grocery shopping', 'category': 'food', 'days_ago': 1},
        {'amount': 120, 'description': 'Coffee and snacks', 'category': 'food', 'days_ago': 1},
        {'amount': 800, 'description': 'Monthly internet bill', 'category': 'Utilities', 'days_ago': 2},
        {'amount': 350, 'description': 'Restaurant dinner', 'category': 'food', 'days_ago': 2},
        {'amount': 2500, 'description': 'Rent payment', 'category': 'Housing', 'days_ago': 3},
        {'amount': 600, 'description': 'Petrol/Gas', 'category': 'Transportation', 'days_ago': 3},
        {'amount': 200, 'description': 'Movie tickets', 'category': 'Entertainment', 'days_ago': 4},
        {'amount': 150, 'description': 'Pharmacy medicines', 'category': 'Healthcare', 'days_ago': 4},
        {'amount': 300, 'description': 'Vegetables and fruits', 'category': 'food', 'days_ago': 5},
        {'amount': 1200, 'description': 'Electricity bill', 'category': 'Utilities', 'days_ago': 6},
        {'amount': 400, 'description': 'Lunch with friends', 'category': 'food', 'days_ago': 7},
        
        # Week 2 (July 10-16, 2025)
        {'amount': 250, 'description': 'Mobile recharge', 'category': 'Utilities', 'days_ago': 8},
        {'amount': 180, 'description': 'Coffee shop', 'category': 'food', 'days_ago': 9},
        {'amount': 500, 'description': 'Clothing shopping', 'category': 'Clothing', 'days_ago': 10},
        {'amount': 320, 'description': 'Dinner at restaurant', 'category': 'food', 'days_ago': 11},
        {'amount': 150, 'description': 'Bus/Metro tickets', 'category': 'Transportation', 'days_ago': 12},
        {'amount': 600, 'description': 'Grocery store', 'category': 'food', 'days_ago': 13},
        {'amount': 800, 'description': 'Car maintenance', 'category': 'Transportation', 'days_ago': 14},
        
        # Week 3 (July 3-9, 2025)
        {'amount': 200, 'description': 'Online shopping', 'category': 'Shopping', 'days_ago': 15},
        {'amount': 400, 'description': 'Weekend grocery', 'category': 'food', 'days_ago': 16},
        {'amount': 150, 'description': 'Snacks and drinks', 'category': 'food', 'days_ago': 17},
        {'amount': 300, 'description': 'Gym membership', 'category': 'Health & Fitness', 'days_ago': 18},
        {'amount': 250, 'description': 'Take-out food', 'category': 'food', 'days_ago': 19},
        {'amount': 180, 'description': 'Book store', 'category': 'Education', 'days_ago': 20},
        {'amount': 500, 'description': 'Weekly groceries', 'category': 'food', 'days_ago': 21},
        
        # Week 4 (June 26 - July 2, 2025)
        {'amount': 350, 'description': 'Restaurant with family', 'category': 'food', 'days_ago': 22},
        {'amount': 120, 'description': 'Morning coffee', 'category': 'food', 'days_ago': 23},
        {'amount': 450, 'description': 'Supermarket shopping', 'category': 'food', 'days_ago': 24},
        {'amount': 200, 'description': 'Movie night', 'category': 'Entertainment', 'days_ago': 25},
        {'amount': 300, 'description': 'Medical checkup', 'category': 'Healthcare', 'days_ago': 26},
        {'amount': 150, 'description': 'Fast food', 'category': 'food', 'days_ago': 27},
        {'amount': 600, 'description': 'Monthly groceries', 'category': 'food', 'days_ago': 28},
        {'amount': 250, 'description': 'Stationery items', 'category': 'Education', 'days_ago': 29},
        {'amount': 400, 'description': 'Weekend shopping', 'category': 'Shopping', 'days_ago': 30},
    ]
    
    print("Adding sample expense data...")
    
    # Clear existing expenses for clean test
    Expense.objects.filter(owner=admin_user).delete()
    
    # Add expenses
    for item in expense_data:
        expense_date = date.today() - timedelta(days=item['days_ago'])
        
        expense = Expense.objects.create(
            amount=item['amount'],
            description=item['description'],
            owner=admin_user,
            category=item['category'],
            date=expense_date
        )
        print(f"Added: {expense_date} - ₹{item['amount']} - {item['description']} ({item['category']})")
    
    print(f"\n✅ Successfully added {len(expense_data)} expenses!")
    
    # Show summary
    total_expenses = Expense.objects.filter(owner=admin_user).count()
    total_amount = sum(float(e.amount) for e in Expense.objects.filter(owner=admin_user))
    avg_amount = total_amount / total_expenses if total_expenses > 0 else 0
    
    print(f"\nSummary:")
    print(f"Total expenses: {total_expenses}")
    print(f"Total amount: ₹{total_amount:,.2f}")
    print(f"Average amount: ₹{avg_amount:.2f}")
    print(f"Date range: {min(e.date for e in Expense.objects.filter(owner=admin_user))} to {max(e.date for e in Expense.objects.filter(owner=admin_user))}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
