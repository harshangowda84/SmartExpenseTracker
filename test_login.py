#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Get admin user
try:
    admin_user = User.objects.get(username='admin')
    print(f"Found admin user: {admin_user.username} ({admin_user.email})")
    
    # Test common passwords
    test_passwords = [
        'admin',
        'password',
        'admin123',
        'password123', 
        '123456',
        'qwerty',
        'admin@123',
        'test123',
        'user123',
        'expense123'
    ]
    
    print("\nTesting common passwords...")
    for password in test_passwords:
        user = authenticate(username='admin', password=password)
        if user:
            print(f"✓ SUCCESS! Password is: '{password}'")
            break
        else:
            print(f"✗ Failed: '{password}'")
    else:
        print("\n❌ None of the common passwords worked.")
        print("You'll need to reset the admin password using:")
        print("python manage.py changepassword admin")
        
except User.DoesNotExist:
    print("No admin user found. Create one with:")
    print("python manage.py createsuperuser")
