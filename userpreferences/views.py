from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from expenses.models import ExpenseLimit
# Create your views here.

@login_required(login_url='/authentication/login')

def index(request):
    # daily_expense_limit=ExpenseLimit.objects.filter(owner=request.user).first()
    daily_expense_limit, created = ExpenseLimit.objects.get_or_create(
        owner=request.user,
        defaults={
            'daily_expense_limit': 5000,
            'monthly_expense_limit': 0
        }
    )
    monthly_expense_limit = daily_expense_limit.monthly_expense_limit
    currency_data = []
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == "GET":
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                currency_data.append({'name': k, 'value': v})

        return render(request, 'preferences/index.html', {
            'currencies': currency_data,
            'user_preferences': user_preferences,
            'daily_expense_limit': daily_expense_limit.daily_expense_limit,
            'monthly_expense_limit': monthly_expense_limit
        })
    else:
        currency = request.POST.get('currency', None)
        daily_expense_limit = request.POST.get('daily_expense_limit', None)
        monthly_expense_limit = request.POST.get('monthly_expense_limit', None)
        # Only update currency if present in POST
        if currency:
            exists = UserPreference.objects.filter(user=request.user).exists()
            if exists:
                user_preferences = UserPreference.objects.get(user=request.user)
                user_preferences.currency = currency
                user_preferences.save()
            else:
                UserPreference.objects.create(user=request.user, currency=currency)
            messages.success(request, f'Currency updated to {currency}')
        # Only update limits if present in POST
        if daily_expense_limit is not None:
            exp_limit, created = ExpenseLimit.objects.get_or_create(owner=request.user)
            exp_limit.daily_expense_limit = daily_expense_limit
            if monthly_expense_limit is not None:
                exp_limit.monthly_expense_limit = monthly_expense_limit
            exp_limit.save()
            messages.success(request, f'Daily expense limit updated to ₹{daily_expense_limit}')
        user_preferences = UserPreference.objects.get(user=request.user) if UserPreference.objects.filter(user=request.user).exists() else None
        exp_limit = ExpenseLimit.objects.get(owner=request.user)
        return render(request, 'preferences/index.html', {
            'currencies': currency_data,
            'user_preferences': user_preferences,
            'daily_expense_limit': exp_limit.daily_expense_limit,
            'monthly_expense_limit': exp_limit.monthly_expense_limit
        })
