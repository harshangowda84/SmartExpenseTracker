# Smart Expense Tracker: Installation Guide

This guide provides detailed step-by-step instructions to install and run the Smart Expense Tracker application on a new machine.

## Prerequisites

### Required Tools

1. **Python 3.10+**
2. **Git** (optional, for cloning the repository)
3. **A text editor or IDE** (VS Code recommended)

## Installation Steps

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/) (version 3.10 or newer)
2. During installation, make sure to check "Add Python to PATH"
3. Verify installation by opening a command prompt/terminal and typing:
   ```
   python --version
   ```

### Step 2: Get the Project Files

**Option 1: Using the ZIP file**
1. Extract the ZIP file to a location of your choice

**Option 2: Using Git**
1. Install Git from [git-scm.com](https://git-scm.com/downloads)
2. Open a terminal and clone the repository:
   ```
   git clone https://github.com/hemantshirsath/Expensetracker.git
   ```

### Step 3: Set Up a Virtual Environment

1. Navigate to the project directory:
   ```
   cd "path/to/Expense Tracker New"
   ```

2. Create a virtual environment:
   ```
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - **Windows**:
     ```
     .venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```
     source .venv/bin/activate
     ```

### Step 4: Install Required Packages

1. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install the NLTK data (required for ML components):
   ```
   python nltk_downloader.py
   ```

### Step 5: Initialize the Database

1. Run migrations to create the database schema:
   ```
   python manage.py migrate
   ```

2. Create a superuser (admin account):
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

3. (Optional) Load sample data:
   ```
   python add_categories.py
   python add_sample_expenses.py
   ```

### Step 6: Run the Development Server

1. Start the Django development server:
   ```
   python manage.py runserver
   ```

2. Open a web browser and go to:
   ```
   http://127.0.0.1:8000/
   ```

3. Log in with the superuser credentials you created earlier or register a new account.

## Project Configuration Options

### Database Configuration (Optional)

The project uses SQLite by default, but supports MySQL. To switch to MySQL:

1. Install the MySQL client library:
   ```
   pip install mysqlclient
   ```

2. Update `expensetracker/settings.py` with your MySQL database settings:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_db_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

### Email Configuration (Optional)

For email functionality (password reset, notifications):

1. Update the email settings in `expensetracker/settings.py`:
   ```python
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_HOST_USER = 'your_email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your_app_password'
   EMAIL_USE_TLS = True
   ```

## Troubleshooting Common Issues

### Package Installation Problems

If you encounter issues installing packages:

```
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Database Migration Issues

If you have migration errors:

```
python manage.py migrate --run-syncdb
```

### NLTK Data Download Issues

If NLTK data doesn't download automatically:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Static Files Not Loading

If CSS or JavaScript files aren't loading:

```
python manage.py collectstatic
```

## Production Deployment Notes

For deploying in a production environment:

1. Set `DEBUG = False` in settings.py
2. Configure a proper production database (PostgreSQL recommended)
3. Set up a proper web server like Nginx or Apache
4. Use Gunicorn or uWSGI as WSGI server
5. Set up proper static file serving
6. Configure SSL for secure connections

---

*Document created: August 7, 2025*  
*For Smart Expense Tracker v2.0*
