# Smart Expense Tracker
![Expense Tracker UI](https://github.com/hemantshirsath/Expensetracker/assets/102463335/f31d97f4-4841-44cb-b2af-62286c60a0c9)
![forecast Expense UI ](https://github.com/hemantshirsath/Expensetracker/assets/102463335/c1188567-39c5-4cc1-8916-24f3d3712ee8)

![forecast Expense UI 2](https://github.com/hemantshirsath/Expensetracker/assets/102463335/a2088949-c4f6-4d18-ba23-308ce3ad19f4)
![report ui Expensewise](https://github.com/hemantshirsath/Expensetracker/assets/102463335/c3271340-d3ea-4171-9618-04c8c0a98759)

## Overview

This is a smart expense tracker web application built using Django. It allows users to log their expenses, categorize them, and provides automated expense categorization and future expense prediction features. This README.md file provides instructions for setting up and running the application on your local machine, as well as some additional information about its features and usage.

## Features

- **Expense Logging**: Easily log your daily expenses, including the date, description, amount, and category.

- **Automated Expense Categorization**: The application uses machine learning algorithms to automatically categorize expenses based on their descriptions. This makes it easier to track and manage your spending.

- **Future Expense Prediction**: The application provides predictions for future expenses based on your spending history. This can help you plan your budget more effectively.

- **User Authentication**: Users can create accounts and log in to securely manage their expenses.

## Setup

✅ **This project has been set up and is ready to run!**

### Prerequisites
- Python 3.13.5 (already configured)
- Virtual environment (already created)
- All dependencies installed

### Quick Start

1. **Run the development server**:
   - Press `Ctrl+Shift+P` in VS Code
   - Type "Tasks: Run Task"
   - Select "Run Django Development Server"
   
   Or run manually in terminal:
   ```bash
   python manage.py runserver
   ```

2. **Open your web browser** and go to `http://localhost:8000` to access the application.

3. **Admin Access**:
   - Admin panel: `http://localhost:8000/admin/`
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: (set password using `python manage.py changepassword admin`)

### Project Features Ready
- ✅ Django 5.1.1 with REST Framework
- ✅ SQLite database with migrations applied
- ✅ Machine learning models (scikit-learn, NLTK) for expense categorization
- ✅ ARIMA time series forecasting (statsmodels)
- ✅ PDF report generation (xhtml2pdf, reportlab)
- ✅ Data visualization (matplotlib, pandas)
- ✅ Multi-currency support
- ✅ User authentication system

### Manual Setup (if needed)
If you need to set up from scratch:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hemantshirsath/Expensetracker.git
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install scikit-learn validate-email xhtml2pdf statsmodels
   ```

4. **Download NLTK data**:
   ```bash
   python nltk_downloader.py
   ```

5. **Run migrations and create superuser**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

## Usage

1. Create a new account or log in using your superuser account.

2. Start logging your expenses by clicking the "Add Expense" button.

3. Fill in the expense details, including the date, description, amount, and category. You can also leave the category empty, and the application will attempt to automatically categorize it.

4. View your expense history, categorized expenses, and future expense predictions on the dashboard.

5. To access the admin panel, go to `http://localhost:8000/admin/` and log in with your superuser credentials. From the admin panel, you can manage users, categories, and view the database.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub.

2. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature-name
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m "Add new feature"
   ```

4. Push your changes to your forked repository:

   ```bash
   git push origin feature-name
   ```

5. Create a pull request on the original repository to propose your changes.

## Acknowledgments

- Thanks to the Django community for creating such a powerful web framework.

- The automated expense categorization and prediction features are powered by machine learning models, which were trained using various open-source libraries and datasets.

Feel free to customize and enhance this smart expense tracker according to your needs. Happy budgeting!
