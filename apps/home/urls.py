from django.urls import path

from django.utils.translation import gettext_lazy as _

from apps.home.views import HomeView

app_name = "home"

urlpatterns = [
    path(
        '',
        HomeView.as_view(),
        name="index"
    )
]