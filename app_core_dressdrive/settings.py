from .general_settings import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

selected_db = os.getenv('DATABASE')

connection_type = os.getenv('CONNECTION_TYPE')

db_conn_max_age = int(os.getenv("DB_CONN_MAX_AGE"))

default_database = {
    'CONN_MAX_AGE': db_conn_max_age,
    'NAME': os.getenv('NAME'),
    'USER': os.getenv('USER_DB'),
    'PASSWORD': os.getenv('PASSWORD'),
    'HOST': os.getenv('HOST')
}

if connection_type == "remote":
    default_database['PORT'] = os.getenv("PORT")

if selected_db == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            **default_database,
        }
    }
elif selected_db == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            **default_database,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR.child(f'{os.getenv("NAME")}.sqlite3'),
        }
    }