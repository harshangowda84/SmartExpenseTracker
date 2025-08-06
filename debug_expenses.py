#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
django.setup()

from expenses.models import Expense
from django.contrib.auth.models import User

try:
    admin_user = User.objects.get(username='admin')
    expenses = Expense.objects.filter(owner=admin_user).order_by('-date')
    
    print(f'Total expenses: {expenses.count()}')
    print('Recent expenses:')
    for e in expenses[:10]:
        print(f'{e.date}: ₹{e.amount} - {e.category} - {e.description}')
        
    if expenses.count() > 0:
        print(f'\nDate range: {expenses.last().date} to {expenses.first().date}')
        print(f'Total amount: ₹{sum(float(e.amount) for e in expenses)}')
        print(f'Average amount: ₹{sum(float(e.amount) for e in expenses) / expenses.count():.2f}')
        
except User.DoesNotExist:
    print("Admin user not found")
except Exception as e:
    print(f"Error: {e}")
