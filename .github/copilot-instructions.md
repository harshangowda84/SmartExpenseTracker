# Copilot Instructions for Smart Expense Tracker

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a Django-based Smart Expense Tracker application with machine learning capabilities for automated expense categorization and prediction.

## Technology Stack
- **Backend**: Django 5.1.1 with Django REST Framework
- **Database**: SQLite (default) with MySQL support
- **Machine Learning**: scikit-learn, NLTK for expense categorization and prediction
- **Data Visualization**: matplotlib, pandas for charts and reports
- **PDF Generation**: reportlab for expense reports
- **Authentication**: Django's built-in authentication system

## Key Features
- User authentication and profile management
- Expense logging and categorization
- Automated expense categorization using ML
- Future expense prediction
- Data visualization and reporting
- Goal setting and tracking
- Multi-currency support

## Project Structure
- `expenses/` - Main expense management app
- `authentication/` - User authentication logic
- `userprofile/` - User profile management
- `expense_forecast/` - ML models for expense prediction
- `report_generation/` - PDF report generation
- `goals/` - Goal setting and tracking
- `userincome/` - Income tracking
- `userpreferences/` - User preferences management
- `api/` - REST API endpoints
- `static/` - Static files (CSS, JS, images)
- `templates/` - Django HTML templates

## Development Guidelines
- Follow Django best practices and conventions
- Use Django's ORM for database operations
- Implement proper error handling and validation
- Maintain clean separation between views, models, and templates
- Use Django's built-in security features
- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add docstrings for complex functions and classes

## Dependencies
Key dependencies include Django, djangorestframework, scikit-learn, pandas, matplotlib, nltk, reportlab, and mysqlclient.
