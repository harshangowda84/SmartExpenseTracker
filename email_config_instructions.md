# Email Configuration Instructions

## Problem
The application was trying to send email notifications when daily expense limits are exceeded, but Gmail authentication was failing.

## Quick Fix Applied
Email notifications are temporarily disabled to prevent app crashes. The warning message is still shown in the web interface.

## To Re-enable Email Notifications (Optional)

### Option 1: Use Gmail App Passwords (Recommended)
1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to https://myaccount.google.com/security
   - Click on "2-Step Verification"
   - Scroll down to "App passwords"
   - Generate a new app password for "Mail"
3. **Update Django Settings**:
   ```python
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-16-character-app-password'
   ```

### Option 2: Use Console Email Backend (for Development)
In `settings.py`, change:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
This will print emails to the console instead of sending them.

### Option 3: Disable Email Completely
Keep the current setup where only warning messages are shown in the web interface.

## Current Behavior
- ✅ Daily expense limit checking still works
- ✅ Warning messages are displayed in the web interface
- ✅ Expenses are still saved properly
- ❌ Email notifications are disabled (no crashes)

## Testing
Try adding an expense above your daily limit to see the improved warning message.
