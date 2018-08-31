import environ

from .base import *  # noqa
from .base import INSTALLED_APPS


INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

COMPRESS_OFFLINE = True

# Create a .env.production file in django's root
environ.Env.read_env('.env.production')
env = environ.Env()

SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': env.db()
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INTERNAL_IPS = env.list('INTERNAL_IPS')

RAVEN_CONFIG = {
    'dsn': env.str('RAVEN_URL'),
}

MAILING_LIST_LIST_ID = env('MAILING_LIST_LIST_ID')
MAILING_LIST_FORM_ACTION = env('MAILING_LIST_FORM_ACTION')
