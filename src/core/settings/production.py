import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa
from .base import CACHES


COMPRESS_OFFLINE = True

# Create a .env.production file in django's root
environ.Env.read_env('.env.production')
env = environ.Env()

ENV_NAME = env('ENV_NAME')

SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': env.db()
}

cache_config = {
    'default': {
        'BACKEND': env('CACHE_BACKEND', default='django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': env('CACHE_LOCATION', default=''),
    }
}
CACHES.update(cache_config)

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

ADMINS = [x.split(':') for x in env.list('ADMINS')]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Piwik goal tracking ids
GOAL_REGISTER_ID = env.int('GOAL_REGISTER_ID')
GOAL_FIRST_LOGIN_ID = env.int('GOAL_FIRST_LOGIN_ID')

# When we generate css files we ALSO generate prefix (-moz-, -wk-, -ms-)
# In local env we only do "make css" command for performances reasons.
SASS_PATH = 'make fullcss'

EMAIL_BACKEND = env('EMAIL_BACKEND')

# For staging, we want to restrict email sending to a whitelist
EMAIL_WHITELIST = env.list('EMAIL_WHITELIST', [])

# Sendinblue api and settings
SIB_API_KEY = env('SIB_API_KEY')
SIB_NEWSLETTER_LIST_IDS = env('SIB_NEWSLETTER_LIST_IDS')
ANYMAIL = {
    'SENDINBLUE_API_KEY': SIB_API_KEY,
}
SIB_EXPORT_CONTACTS_LIST_ID = env.int('SIB_EXPORT_CONTACTS_LIST_ID')
SIB_WELCOME_EMAIL_ENABLED = env.bool('SIB_WELCOME_EMAIL_ENABLED')
SIB_WELCOME_EMAIL_TEMPLATE_ID = env.int('SIB_WELCOME_EMAIL_TEMPLATE_ID')
SIB_PUBLICATION_EMAIL_ENABLED = env.bool('SIB_PUBLICATION_EMAIL_ENABLED')
SIB_PUBLICATION_EMAIL_TEMPLATE_ID = env.int('SIB_PUBLICATION_EMAIL_TEMPLATE_ID')
SIB_ALERT_CONFIRMATION_EMAIL_TEMPLATE_ID = env.int('SIB_ALERT_CONFIRMATION_EMAIL_TEMPLATE_ID')

EXPORT_CONTACTS_ENABLED = env.bool('EXPORT_CONTACTS_ENABLED')

# File storage settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

ENABLE_AID_LIST_API_CACHE = env.bool('ENABLE_AID_LIST_API_CACHE', False)
AID_LIST_API_CACHE_TIMEOUT = env.int('AID_LIST_API_CACHE_TIMEOUT', 0)
ENABLE_AID_DETAIL_API_CACHE = env.bool('ENABLE_AID_DETAIL_API_CACHE', False)
AID_DETAIL_API_CACHE_TIMEOUT = env.int('AID_DETAIL_API_CACHE_TIMEOUT', 0)
