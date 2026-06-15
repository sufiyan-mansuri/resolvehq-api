from .base import *

SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'resolvehq',
        'USER': 'postgres',
        'PASSWORD': 'sfynm17,',
        'HOST': 'localhost',      
        'PORT': '5432',
    }
}

CORS_ALLOW_ALL_ORIGINS = True