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

ANALYTICS_ENABLED = env.bool('ANALYTICS_ENABLED')

ANALYTICS_SITEID = env('ANALYTICS_SITEID')

CONTACT_EMAIL = env('CONTACT_EMAIL')

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_FILE_PATH = '/tmp/django_emails'
