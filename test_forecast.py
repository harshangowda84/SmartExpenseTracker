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
from expense_forecast.views import forecast
from django.test import RequestFactory
from django.contrib.auth import login

# Create a test request with authenticated user
factory = RequestFactory()
admin_user = User.objects.get(username='admin')

# Create a fake request object
request = factory.get('/forecast/')
request.user = admin_user

try:
    print("Testing forecast function directly...")
    
    # Import the required modules for the forecast
    import numpy as np
    import pandas as pd
    from django.utils.timezone import now
    from datetime import datetime, timedelta
    
    # Get expense data like in the forecast function
    expenses = Expense.objects.filter(owner=admin_user).order_by('-date')[:60]
    print(f"Found {expenses.count()} expenses for user {admin_user.username}")
    
    if expenses.count() >= 5:
        # Create a DataFrame from the expenses
        data = pd.DataFrame({
            'Date': [expense.date for expense in expenses], 
            'Expenses': [float(expense.amount) for expense in expenses], 
            'Category': [expense.category for expense in expenses]
        })
        data.set_index('Date', inplace=True)
        data = data.sort_index()
        
        print(f"Data shape: {data.shape}")
        print(f"Date range: {data.index.min()} to {data.index.max()}")
        print(f"Expense range: ₹{data['Expenses'].min():.2f} to ₹{data['Expenses'].max():.2f}")
        print(f"Average expense: ₹{data['Expenses'].mean():.2f}")
        
        # Try the simple forecasting approach
        forecast_steps = 30
        recent_expenses = data['Expenses'].tail(10)
        weekly_avg = recent_expenses.mean()
        print(f"Weekly average: ₹{weekly_avg:.2f}")
        
        # Calculate trend
        if len(recent_expenses) >= 7:
            early_avg = recent_expenses.head(5).mean()
            late_avg = recent_expenses.tail(5).mean()
            trend = (late_avg - early_avg) / 5
        else:
            trend = 0
        
        print(f"Calculated trend: ₹{trend:.2f} per day")
        
        # Generate forecast
        forecast_values = []
        for i in range(forecast_steps):
            predicted_amount = max(0, weekly_avg + (i * trend * 0.1))
            forecast_values.append(predicted_amount)
        
        print(f"First 5 forecast values: {[f'₹{v:.2f}' for v in forecast_values[:5]]}")
        print(f"Total forecasted expenses: ₹{sum(forecast_values):.2f}")
        print(f"Average daily forecast: ₹{sum(forecast_values)/len(forecast_values):.2f}")
        
        print("✅ Forecast calculation successful!")
        
    else:
        print(f"❌ Not enough expenses for forecasting. Found: {expenses.count()}, needed: 5")
        
except Exception as e:
    import traceback
    print(f"❌ Error during forecast test: {type(e).__name__}: {str(e)}")
    print(f"Full traceback:\n{traceback.format_exc()}")
