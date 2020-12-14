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

ENV_NAME = env('ENV_NAME')

SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': env.db()
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INTERNAL_IPS = env.list('INTERNAL_IPS')

CELERY_BROKER_URL = env('CELERY_BROKER_URL')

RAVEN_CONFIG = {
    'dsn': env.str('RAVEN_URL'),
}

MAILING_LIST_URL = env('MAILING_LIST_URL')

ANALYTICS_ENABLED = env.bool('ANALYTICS_ENABLED')

ANALYTICS_SITEID = env('ANALYTICS_SITEID')

HOTJAR_SITEID = env('HOTJAR_SITEID')

CONTACT_EMAIL = env('CONTACT_EMAIL')
CONTACT_PHONE = env('CONTACT_PHONE')

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_FILE_PATH = '/tmp/django_emails'

ADMINS = [x.split(':') for x in env.list('ADMINS')]

# For staging only, this will be ignored in production
EMAIL_WHITELIST = env.list('EMAIL_WHITELIST', [])

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Piwik goal tracking ids
GOAL_REGISTER_ID = env.int('GOAL_REGISTER_ID')
GOAL_FIRST_LOGIN_ID = env.int('GOAL_FIRST_LOGIN_ID')

SASS_PATH = 'make fullcss'

# Sendinblue api and settings
SIB_API_KEY = env('SIB_API_KEY')
SIB_LIST_ID = env.int('SIB_LIST_ID')
