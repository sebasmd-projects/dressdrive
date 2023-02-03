"""
Django settings for app_core_dressdrive project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
# Provides a way of using operating system dependent functionality.
import os

# In this file is used to convert string to python list
import ast

# Is a function from the dotenv library that reads the values from a .env file and sets them as environment variables in your application.
from dotenv import load_dotenv

# Provides classes for working with dates and times.
import datetime

# Provides functions for encoding and decoding JSON data.
import json

# Provides a convenient way of working with file system paths.
from unipath import Path

# Is a function from the Django internationalization (i18n)
# framework that allows for lazy translation of string values.
# The _ alias for gettext_lazy is a common convention in Django code.
from django.utils.translation import gettext_lazy as _

# Is an exception that is raised by Django when there is a problem with the configuration of the project,
# such as missing required settings.
# This exception can be caught and handled in the code to provide a custom error message or take other appropriate action.
from django.core.exceptions import ImproperlyConfigured

# Load environment variables from a .env file in the application
load_dotenv()

file = ""

# Build paths inside the project like this: BASE_DIR.child('public','templates') = public/templates.
BASE_DIR = Path(__file__).ancestor(2)
file += f"{BASE_DIR}"

# Locale folder
LOCALE_PATHS = (BASE_DIR.child('public', 'locale'),)

# Select the environment
environment = os.getenv('ENVIRONMENT')

# Global URL
BASE_URL = json.loads(os.getenv('BASE_URL'))[environment]

# User model
AUTH_USER_MODEL = os.getenv('AUTH_USER_MODEL')

# Session expire cookies
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode
if environment == 'prod':
    DEBUG = False
else:
    DEBUG = True

# Allowed Hosts
ALLOWED_HOSTS = json.loads(os.getenv('ALLOWED_HOSTS'))[environment]

# Cors Allowed Origins
CORS_ALLOWED_ORIGINS = json.loads(
    os.getenv('CORS_ALLOWED_ORIGINS'))[environment]

# SSL Redirect
if environment == 'prod':
    SECURE_SSL_REDIRECT = True
else:
    SECURE_SSL_REDIRECT = False

# Email Configuration
# https://docs.djangoproject.com/en/4.1/topics/email/
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')

# Email security
if os.getenv('EMAIL_SECURITY_CONNECTION').upper() == 'SSL':
    EMAIL_USE_SSL = True
elif os.getenv('EMAIL_SECURITY_CONNECTION').upper() == 'TLS':
    EMAIL_USE_TLS = True
else:
    raise ImproperlyConfigured(
        "You must choose SSL or TLS"
    )

# Email Host
EMAIL_HOST = os.getenv('EMAIL_HOST')

# Email Port
EMAIL_PORT = os.getenv('EMAIL_PORT')

# Email User
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

# Email Password
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Email Default From
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Application definition
# Django Apps
DJANGO_APPS = ast.literal_eval(os.getenv('DJANGO_APPS'))

# Third-party Apps
THIRD_PARTY_APPS = ast.literal_eval(os.getenv('THIRD_PARTY_APPS'))

# Local Apps
LOCAL_APPS = ast.literal_eval(os.getenv('LOCAL_APPS'))

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
    'django.middleware.locale.LocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Main urls.py file
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
ROOT_URLCONF = os.getenv('ROOT_URLCONF')

# WSGI aplication
WSGI_APPLICATION = os.getenv('WSGI_APPLICATION')


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
selected_db = os.getenv('DATABASE')

connection_type = os.getenv('CONNECTION_TYPE')

default_database = {
    'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE')),
    'NAME': os.getenv('NAME'),
    'USER': os.getenv('USER_DB'),
    'PASSWORD': os.getenv('PASSWORD'),
    'HOST': os.getenv('HOST')
}

if connection_type == "local":
    database_config = {
        **default_database,
    }
else:
    database_config = {
        'PORT': os.getenv('PORT'),
        **default_database
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
            'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE')),
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR.child(f'{os.getenv("NAME")}.sqlite3'),
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
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE')

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]

TIME_ZONE = os.getenv('TIME_ZONE')

USE_I18N = True

USE_TZ = True

USE_L10N = True


SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
# Where are you going to copy the files to?
if environment == 'local':
    STATIC_ROOT = BASE_DIR.child('public', 'static')
else:
    STATIC_ROOT = os.getenv('STATIC_ROOT')

# Where you copy the app files from?
STATICFILES_DIRS = [BASE_DIR.child('static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = 'public/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Athentication method
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'apps.authentication.login.backend.EmailOrUsernameModelBackend'
)


ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": f"{os.getenv('SOCIALACCOUNT_PROVIDERS_client_id')}",
            "secret": f"{os.getenv('SOCIALACCOUNT_PROVIDERS_secret')}",
            "key": f"{os.getenv('SOCIALACCOUNT_PROVIDERS_key')}"
        }
    }
}

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
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(
        days=int(os.getenv('ACCESS_TOKEN_LIFETIME'))
    )
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
