#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
django.setup()

from expenses.models import Expense
from django.contrib.auth.models import User

try:
    user = User.objects.get(username='admin')
    expenses = Expense.objects.filter(owner=user)
    print(f"Total expenses for admin: {expenses.count()}")
    
    if expenses.exists():
        print("\nRecent expenses:")
        for expense in expenses.order_by('-date')[:10]:
            print(f"{expense.date}: ₹{expense.amount} - {expense.category} - {expense.description}")
    else:
        print("No expenses found. You need to add some expenses first.")
        
except User.DoesNotExist:
    print("Admin user not found")
except Exception as e:
    print(f"Error: {e}")
