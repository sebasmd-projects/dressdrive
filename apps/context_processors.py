from django.conf import settings
from django.urls import reverse

def custom_processors(request):
    ctx = {}
    ctx['base_url'] = settings.BASE_URL
    # Login
    ctx['login_url'] = reverse('authentication_login:user-login')
    ctx['logout_url'] = reverse('authentication_login:user-logout')
    # Register
    ctx['register_url'] = reverse('authentication_register:user-register')
    # User
    ctx['change_password_url'] = reverse('settings_user:user_change_password')
    ctx['change_email_url'] = reverse('settings_user:user_change_email')
    ctx['change_profile_url'] = reverse('settings_user:user_change_profile')
    ctx['change_notifications_url'] = reverse('settings_user:user_change_notifications')
    ctx['reset_password'] = reverse('settings_user:user_password_reset')
    return ctx