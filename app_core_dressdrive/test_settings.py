from .general_settings import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.child(f'test_{os.getenv("NAME")}.sqlite3'),
    }
}