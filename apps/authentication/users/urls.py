from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.authentication.users import views

app_name = "settings_user"

urlpatterns = [
    path(
        _('change-password/'),
        views.UpdatePasswordView.as_view(),
        name='user_change_password'
    ),
    path(
        _('change-email/'),
        views.UpdateEmailView.as_view(),
        name='user_change_email'
    ),
    path(
        _('change-profile/'),
        views.UpdateProfileView.as_view(),
        name='user_change_profile'
    ),
    path(
        _('change-notifications/'),
        views.UpdateNotificationsView.as_view(),
        name='user_change_notifications'
    ),
    path(
        _('reset-password/'),
        views.PasswordResetView.as_view(),
        name='user_password_reset'
    ),
]

"""
path(
    _('reset-password/done/'),
    views..as_view(),
    name='password_reset_done'
),
path(
    _('reset-password/complete/'),
    views..as_view(),
    name='password_reset_complete'
),

"""
