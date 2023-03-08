"""app_core_dressdrive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# import admin url patterns
from django.contrib import admin

#
from django.urls import path, include

# show static and media files
from django.conf import settings
from django.conf.urls.static import static

#
from django.utils.translation import gettext_lazy as _

# Set the API documentation with drf_yasg
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="DressDrive - ApiDoc",
        default_version='v1.0.0',
        description=_("DressDrive App API documentation"),
        terms_of_service=f"{settings.BASE_URL}/policies/terms/",
        contact=openapi.Contact(email=f"{settings.EMAIL_HOST_USER}"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


admin_urlpatterns = [
    path(
        'admin/site/',
        admin.site.urls
    )
]

third_party_url_patterns = [
    path(
        '__debug__/',
        include('debug_toolbar.urls')
    ),
    path(
        'api/docs/',
        schema_view.with_ui(
            'swagger',
            cache_timeout=0
        ),
        name='schema-swagger-ui'
    ),
    path(
        'api-auth/',
        include('rest_framework.urls')
    )
]

custom_apps_url_patterns = [
    path(
        'accounts/',
        include('apps.authentication.login.urls')
    ),
    path(
        'accounts/',
        include('apps.authentication.register.urls')
    ),
    path(
        'accounts/',
        include('apps.authentication.users.urls')
    ),
    path(
        '',
        include('apps.home.urls')
    )
]

urlpatterns = admin_urlpatterns + \
    third_party_url_patterns + \
    custom_apps_url_patterns + \
    static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

handler400 = "apps.status_errors.views.handler400"
handler403 = "apps.status_errors.views.handler403"
handler404 = "apps.status_errors.views.handler404"
handler500 = "apps.status_errors.views.handler500"
