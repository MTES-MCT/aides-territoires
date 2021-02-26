import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa
from .base import INSTALLED_APPS


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

sentry_sdk.init(
    dsn=env.str('SENTRY_URL'),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

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

# For staging, we want to restrict email sending to a whitelist
EMAIL_WHITELIST = env.list('EMAIL_WHITELIST', [])
ENABLE_EMAIL_WHITELIST = env.bool('ENABLE_EMAIL_WHITELIST', False)

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
ANYMAIL = {
    'SENDINBLUE_API_KEY': SIB_API_KEY,
}
SIB_WELCOME_EMAIL_ENABLED = env.bool('SIB_WELCOME_EMAIL_ENABLED')
SIB_WELCOME_EMAIL_TEMPLATE_ID = env.int('SIB_WELCOME_EMAIL_TEMPLATE_ID')
SIB_PUBLICATION_EMAIL_ENABLED = env.bool('SIB_PUBLICATION_EMAIL_ENABLED')
SIB_PUBLICATION_EMAIL_TEMPLATE_ID = env.int('SIB_PUBLICATION_EMAIL_TEMPLATE_ID')

# File storage settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL = 'public-read'
