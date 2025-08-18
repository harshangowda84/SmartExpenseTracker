from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pytesseract
from PIL import Image
import io
# OCR extraction API view
@csrf_exempt
def extract_ocr(request):
    if request.method == 'POST' and request.FILES.get('bill_image'):
        image_file = request.FILES['bill_image']
        try:
            image = Image.open(image_file)
            text = pytesseract.image_to_string(image)
            return JsonResponse({'text': text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
from django.views.decorators.csrf import csrf_exempt

# AJAX endpoint for OCR extraction
@csrf_exempt
def extract_expense_data(request):
    if request.method == 'POST' and request.FILES.get('bill_image'):
        bill_image = request.FILES['bill_image']
        try:
            image = Image.open(bill_image)
            ocr_text = pytesseract.image_to_string(image)
            import re
            nlp = spacy.load('en_core_web_sm')
            doc = nlp(ocr_text)
            merchant = None
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    merchant = ent.text
                    break
            if not merchant:
                lines = ocr_text.splitlines()
                merchant = lines[0] if lines else ''
            # Improved extraction: prioritize 'Total' value
            # Use spaCy MONEY entity extraction for amount
            extracted_amount = ''
            money_entities = []
            for ent in doc.ents:
                if ent.label_ == 'MONEY':
                    # Only consider if currency symbol present and not in GST/invoice/table lines
                    if re.search(r'[₹Rs]', ent.text):
                        if not re.search(r'GST|invoice|table', ent.sent.text, re.IGNORECASE):
                            val = re.sub(r'[^\d.,]', '', ent.text)
                            try:
                                money_entities.append(float(val.replace(',', '')))
                            except:
                                pass
            if money_entities:
                extracted_amount = str(int(max(money_entities)))
            else:
                # Fallback to previous logic if no MONEY entities found
                lines = ocr_text.splitlines()
                total_amounts = []
                for line in lines:
                    if re.search(r'Total|Sub-Total', line, re.IGNORECASE):
                        # Only consider numbers with currency symbol and not in GST/invoice/table lines
                        if not re.search(r'GST|invoice|table', line, re.IGNORECASE):
                            total_amounts += re.findall(r'[₹Rs]\s*(\d{3,6}[.,]?\d*)', line)
                total_amounts = [float(a.replace(',', '')) for a in total_amounts if a and float(a.replace(',', '')) > 100]
                if total_amounts:
                    extracted_amount = str(int(max(total_amounts)))
                else:
                    # Fallback: find all currency-like numbers in lines with ₹ or Rs, excluding GST/invoice/table lines
                    currency_lines = [l for l in lines if re.search(r'[₹Rs]', l) and not re.search(r'GST|invoice|table', l, re.IGNORECASE)]
                    amounts = []
                    for l in currency_lines:
                        amounts += re.findall(r'[₹Rs]\s*(\d{3,6}[.,]?\d*)', l)
                    filtered = [float(a.replace(',', '')) for a in amounts if a and float(a.replace(',', '')) > 100]
                    if filtered:
                        extracted_amount = str(int(max(filtered)))
            date_match = re.search(r'(\d{2}[/-]\d{2}[/-]\d{4})', ocr_text)
            if date_match:
                extracted_date = date_match.group(1)
            else:
                extracted_date = None
                for ent in doc.ents:
                    if ent.label_ == 'DATE':
                        extracted_date = ent.text
                        break
            extracted_description = merchant
            if extracted_description:
                clean_desc = preprocess_text(extracted_description)
                desc_vec = tfidf_vectorizer.transform([clean_desc])
                predicted_category = model.predict(desc_vec)[0]
            else:
                predicted_category = 'Uncategorized'
            return JsonResponse({
                'success': True,
                'ocr_text': ocr_text,
                'amount': extracted_amount or '',
                'description': extracted_description or '',
                'expense_date': extracted_date or '',
                'category': predicted_category
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'OCR failed: {str(e)}'})
    return JsonResponse({'success': False, 'error': 'No image uploaded.'})
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime
import requests
import pandas as pd
import pytesseract
import spacy
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from django.contrib.sessions.models import Session
from datetime import date
import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from .models import ExpenseLimit
from django.core.mail import send_mail
from django.conf import settings
data = pd.read_csv('dataset.csv')

# Preprocessing
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
    return ' '.join(tokens)

data['clean_description'] = data['description'].apply(preprocess_text)

# Feature extraction
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(data['clean_description'])

# Train a RandomForestClassifier
model = RandomForestClassifier()
model.fit(X, data['category'])
@login_required(login_url='/authentication/login')
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)

    sort_order = request.GET.get('sort')

    if sort_order == 'amount_asc':
        expenses = expenses.order_by('amount')
    elif sort_order == 'amount_desc':
        expenses = expenses.order_by('-amount')
    elif sort_order == 'date_asc':
        expenses = expenses.order_by('date')
    elif sort_order == 'date_desc':
        expenses = expenses.order_by('-date')

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except:
        currency=None

    total = page_obj.paginator.num_pages
    # Check daily expense limit and show warning if exceeded
    user = request.user
    expense_limits = ExpenseLimit.objects.filter(owner=user)
    if expense_limits.exists():
        daily_expense_limit = expense_limits.first().daily_expense_limit
    else:
        daily_expense_limit = 5000
    total_expenses_today = get_expense_of_day(user)
    if daily_expense_limit > 0 and total_expenses_today > daily_expense_limit:
        messages.warning(request, f'Your expenses for today (₹{total_expenses_today}) exceed your daily expense limit of ₹{daily_expense_limit}.')

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
        'total': total,
        'sort_order': sort_order,
    }
    return render(request, 'expenses/index.html', context)

daily_expense_amounts = {}

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        # OCR logic for bill image
        bill_image = request.FILES.get('bill_image')
        ocr_text = None
        extracted_amount = None
        extracted_description = None
        extracted_date = None
        extracted_category = None
        if bill_image:
            try:
                image = Image.open(bill_image)
                ocr_text = pytesseract.image_to_string(image)
                import re
                # Load spaCy model
                nlp = spacy.load('en_core_web_sm')
                doc = nlp(ocr_text)
                # Extract merchant (first ORG entity or first line)
                merchant = None
                for ent in doc.ents:
                    if ent.label_ == 'ORG':
                        merchant = ent.text
                        break
                if not merchant:
                    lines = ocr_text.splitlines()
                    merchant = lines[0] if lines else ''
                # Extract amount
                amount_match = re.search(r'(?:total|amount|amt)[^\d]*(\d+[.,]?\d*)', ocr_text, re.IGNORECASE)
                if amount_match:
                    extracted_amount = amount_match.group(1)
                else:
                    # fallback: first currency-like number
                    currency_match = re.search(r'(\d+[.,]\d{2})', ocr_text)
                    if currency_match:
                        extracted_amount = currency_match.group(1)
                # Extract date
                date_match = re.search(r'(\d{2}[/-]\d{2}[/-]\d{4})', ocr_text)
                if date_match:
                    extracted_date = date_match.group(1)
                else:
                    # fallback: first DATE entity
                    for ent in doc.ents:
                        if ent.label_ == 'DATE':
                            extracted_date = ent.text
                            break
                # Use merchant as description
                extracted_description = merchant
                # ML-based category prediction using trained model
                if extracted_description:
                    # Preprocess description
                    clean_desc = preprocess_text(extracted_description)
                    desc_vec = tfidf_vectorizer.transform([clean_desc])
                    predicted_category = model.predict(desc_vec)[0]
                else:
                    predicted_category = 'Uncategorized'
                context['values'] = {
                    'amount': extracted_amount or '',
                    'description': extracted_description or '',
                    'expense_date': extracted_date or '',
                    'category': predicted_category
                }
                messages.info(request, 'OCR scan complete. Please review and submit the details.')
                return render(request, 'expenses/add_expense.html', context)
            except Exception as e:
                messages.error(request, f'OCR failed: {str(e)}')
                return render(request, 'expenses/add_expense.html', context)

        # If no image, proceed with normal form
        amount = request.POST['amount']
        date_str = request.POST.get('expense_date')
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        predicted_category = request.POST['category']
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            today = datetime.date.today()
            if date > today:
                messages.error(request, 'Date cannot be in the future')
                return render(request, 'expenses/add_expense.html', context)
            user = request.user
            expense_limits = ExpenseLimit.objects.filter(owner=user)
            if expense_limits.exists():
                daily_expense_limit = expense_limits.first().daily_expense_limit
            else:
                daily_expense_limit = 5000
            total_expenses_today = get_expense_of_day(user) + float(amount)
            if daily_expense_limit > 0 and total_expenses_today > daily_expense_limit:
                messages.warning(request, f'Your expenses for today (₹{total_expenses_today}) exceed your daily expense limit of ₹{daily_expense_limit}.')
            Expense.objects.create(owner=request.user, amount=amount, date=date,
                                   category=predicted_category, description=description)
            messages.success(request, 'Expense saved successfully')
            return redirect('expenses')
        except ValueError:
            messages.error(request, 'Invalid date format')
            return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        date_str = request.POST.get('expense_date')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        try:
            # Convert the date string to a datetime object and validate the date
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            today = datetime.date.today()

            if date > today:
                messages.error(request, 'Date cannot be in the future')
                return render(request, 'expenses/edit-expense.html', context)

            expense.owner = request.user
            expense.amount = amount
            expense. date = date
            expense.category = category
            expense.description = description

            expense.save()
            messages.success(request, 'Expense saved successfully')

            return redirect('expenses')
        except ValueError:
            messages.error(request, 'Invalid date format')
            return render(request, 'expenses/edit-expense.html', context)

        # expense.owner = request.user
        # expense.amount = amount
        # expense. date = date
        # expense.category = category
        # expense.description = description

        # expense.save()

        # messages.success(request, 'Expense updated  successfully')

        # return redirect('expenses')

@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')

@login_required(login_url='/authentication/login')
def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

@login_required(login_url='/authentication/login')
def stats_view(request):
    return render(request, 'expenses/stats.html')

@login_required(login_url='/authentication/login')
def predict_category(description):
    predict_category_url = 'http://localhost:8000/api/predict-category/'  # Use the correct URL path
    data = {'description': description}
    response = requests.post(predict_category_url, data=data)

    if response.status_code == 200:
        # Get the predicted category from the response
        predicted_category = response.json().get('predicted_category')
        return predicted_category
    else:
        # Handle the case where the prediction request failed
        return None
    

def set_expense_limit(request):
    if request.method == "POST":
        daily_expense_limit = request.POST.get('daily_expense_limit')
        monthly_expense_limit = request.POST.get('monthly_expense_limit')
        # Validate daily limit
        if not daily_expense_limit or daily_expense_limit.strip() == '':
            messages.error(request, "Please enter a valid daily expense limit.")
            return HttpResponseRedirect('/preferences/')
        try:
            daily_expense_limit_int = int(daily_expense_limit)
            if daily_expense_limit_int < 0:
                messages.error(request, "Daily expense limit must be zero or greater.")
                return HttpResponseRedirect('/preferences/')
        except ValueError:
            messages.error(request, "Please enter a valid number for daily expense limit.")
            return HttpResponseRedirect('/preferences/')
        # Validate monthly limit
        if not monthly_expense_limit or monthly_expense_limit.strip() == '':
            messages.error(request, "Please enter a valid monthly expense limit.")
            return HttpResponseRedirect('/preferences/')
        try:
            monthly_expense_limit_int = int(monthly_expense_limit)
            if monthly_expense_limit_int < 0:
                messages.error(request, "Monthly expense limit must be zero or greater.")
                return HttpResponseRedirect('/preferences/')
        except ValueError:
            messages.error(request, "Please enter a valid number for monthly expense limit.")
            return HttpResponseRedirect('/preferences/')
        existing_limit = ExpenseLimit.objects.filter(owner=request.user).first()
        if existing_limit:
            existing_limit.daily_expense_limit = daily_expense_limit_int
            existing_limit.monthly_expense_limit = monthly_expense_limit_int
            existing_limit.save()
        else:
            ExpenseLimit.objects.create(owner=request.user, daily_expense_limit=daily_expense_limit_int, monthly_expense_limit=monthly_expense_limit_int)
        messages.success(request, "Expense Limits Updated Successfully!")
        return HttpResponseRedirect('/preferences/')
    else:
        return HttpResponseRedirect('/preferences/')
    
def get_expense_of_day(user):
    current_date=date.today()
    expenses=Expense.objects.filter(owner=user,date=current_date)
    total_expenses=sum(expense.amount for expense in expenses)
    return total_expenses
