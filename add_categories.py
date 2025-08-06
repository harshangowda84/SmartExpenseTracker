#!/usr/bin/env python
import os
import sys
import django

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
django.setup()

from expenses.models import Category

# List of common expense categories
categories = [
    'Food & Dining',
    'Transportation',
    'Shopping',
    'Entertainment',
    'Bills & Utilities',
    'Healthcare',
    'Education',
    'Travel',
    'Groceries',
    'Gas & Fuel',
    'Home & Maintenance',
    'Clothing',
    'Personal Care',
    'Insurance',
    'Charity',
    'Investment',
    'Fees & Charges',
    'Subscription',
    'Other'
]

# Check existing categories
existing_categories = Category.objects.all()
print(f"Existing categories: {[cat.name for cat in existing_categories]}")

# Add categories if they don't exist
for category_name in categories:
    category, created = Category.objects.get_or_create(name=category_name)
    if created:
        print(f"Added category: {category_name}")
    else:
        print(f"Category already exists: {category_name}")

print(f"\nTotal categories in database: {Category.objects.count()}")
