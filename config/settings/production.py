from .base import *
import dj_database_url

SECRET_KEY = env('SECRET_KEY')

if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ['resolvehq.onrender.com']

DATABASES = {
    'default': dj_database_url.parse(env('DATABASE_URL'))
}