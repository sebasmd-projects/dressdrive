from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.authentication.login import views

app_name = "authentication_login"

urlpatterns = [
    path(
        _('login/'),
        views.UserLoginView.as_view(),
        name='user-login'
    ),
    path(
        _('logout/'),
        views.UserLogoutView.as_view(),
        name='user-logout'
    )
]
