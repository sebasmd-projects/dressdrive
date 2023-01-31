from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.authentication.register import views


app_name = "authentication_register"

urlpatterns = [
    path(
        _('register/'), 
        views.UserRegisterView.as_view(), 
        name='user-register',
    ),
]