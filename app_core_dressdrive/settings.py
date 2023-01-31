"""
Django settings for app_core_dressdrive project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
# Validation methods
from typing import Any

# Date and time library
import datetime

# Json utilities
import json

# Manage paths inside the project
from unipath import Path

# Django internationalization
from django.utils.translation import gettext_lazy as _

# Django exceptions
from django.core.exceptions import ImproperlyConfigured

# Open json file
with open("data.json") as f:
    value = json.loads(f.read())


def get_value(value_title: str, values: dict = value) -> Any:
    """ Retrieve a value from the `values` dictionary, based on its `value_title` key.

     Args:
    - value_title (str): The key to look for in the `values` dictionary.
    - values (dict, optional): The dictionary to search for the value. Defaults to `value` (from the json file).

    Raises:
    - ImproperlyConfigured: If the `value_title` key is not found in the `values` dictionary.

    Returns:
    - Any: The value corresponding to the `value_title` key in the `values` dictionary.
    """
    try:
        return values[value_title]
    except:
        msg = _(f"The name of {value_title} doesn't exists")
        raise ImproperlyConfigured(msg)


# Build paths inside the project like this: BASE_DIR.child('public','templates') = public/templates.
BASE_DIR = Path(__file__).ancestor(2)

# Locale folder
LOCALE_PATHS = (BASE_DIR.child('public', 'locale'),)

# Select the environment
environment = get_value('ENVIRONMENT')

# Global URL
BASE_URL = get_value('BASE_URL')[environment]

# User model
AUTH_USER_MODEL = get_value('AUTH_USER_MODEL')

# Athentication method
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'apps.authentication.login.backend.EmailOrUsernameModelBackend',
)

# Session expire cookies
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dirpd&)0o=!mhi$8bgz@r7!ngf@^bn8!arcd*c5mrig53%s(^m'

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode
if environment == 'prod':
    DEBUG = False
else:
    DEBUG = True

# Allowed Hosts
ALLOWED_HOSTS = get_value('ALLOWED_HOSTS')[environment]

# Cors Allowed Origins
CORS_ALLOWED_ORIGINS = get_value('CORS_ALLOWED_ORIGINS')[environment]

# SSL Redirect
if environment == 'prod':
    SECURE_SSL_REDIRECT = True
else:
    SECURE_SSL_REDIRECT = False

# Email Configuration
# https://docs.djangoproject.com/en/4.0/topics/email/
EMAIL_BACKEND = get_value('EMAIL_BACKEND')

# Email security
if get_value('EMAIL_SECURITY_CONNECTION').upper() == 'SSL':
    EMAIL_USE_SSL = True
elif get_value('EMAIL_SECURITY_CONNECTION').upper() == 'TLS':
    EMAIL_USE_TLS = True
else:
    raise ImproperlyConfigured("You must choose SSL or TLS in the data.json file")

# Email Host
EMAIL_HOST = get_value('EMAIL_HOST')

# Email Port
EMAIL_PORT = get_value('EMAIL_PORT')

# Email User
EMAIL_HOST_USER = get_value('EMAIL_HOST_USER')

# Email Password
EMAIL_HOST_PASSWORD = get_value('EMAIL_HOST_PASSWORD')

# Email Default From
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Application definition
# Django Apps
DJANGO_APPS = get_value('DJANGO_APPS')

# Third-party Apps
THIRD_PARTY_APPS = get_value('THIRD_PARTY_APPS')

# Local Apps
LOCAL_APPS = get_value('LOCAL_APPS')

# Join all apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'app_core_dressdrive.urls'

# Templates manager
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('public', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom context processors
                'apps.context_processors.custom_processors',
            ],
        },
    },
]

# Root path
ROOT_URLCONF = get_value('ROOT_URLCONF')

# WSGI aplication
WSGI_APPLICATION = get_value('WSGI_APPLICATION')


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

selected_db = get_value('DATABASE')

database_config = {
    'CONN_MAX_AGE': get_value('DB_CONN_MAX_AGE'),
    'NAME': get_value('NAME'),
    'USER': get_value('USER'),
    'PASSWORD': get_value('PASSWORD'),
    'HOST': get_value('HOST'),
    'PORT': get_value('PORT'),
}

if selected_db == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            **database_config,
        }
    }
elif selected_db == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            **database_config,
        }
    }
else:
    DATABASES = {
        'default': {
            'CONN_MAX_AGE': get_value('DB_CONN_MAX_AGE'),
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR.child(f'{get_value("NAME")}.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = get_value('LANGUAGE_CODE')

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]

TIME_ZONE = get_value('TIME_ZONE')

USE_I18N = True

USE_TZ = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.child('public', 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = 'public/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework Config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    )
}

# SIMPLE_JWT Config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=get_value('ACCESS_TOKEN_LIFETIME'))
}

# SWAGGER Config
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
