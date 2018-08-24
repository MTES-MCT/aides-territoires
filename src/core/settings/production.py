import environ

from .base import *  # noqa


# Create a .env.production file in django's root
environ.Env.read_env('.env.production')
env = environ.Env()

SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': env.db()
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INTERNAL_IPS = env.list('INTERNAL_IPS')
