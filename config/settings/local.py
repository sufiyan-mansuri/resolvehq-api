from .base import *

SECRET_KEY = env('SECRET_KEY')

if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False

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

