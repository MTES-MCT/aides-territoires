from pathlib import Path

import dj_database_url
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa
from .base import TEMPLATES, CACHES


# Sometime, we want to load Scalingo environment from a dotenv file.
# This is specially useful when testing Scalingo setup from a local dev
if Path('.env.scalingo').exists():
    environ.Env.read_env('.env.scalingo')

env = environ.Env()

ENV_NAME = env('ENV_NAME')

SETTINGS_DIR = Path(__file__).parent
CORE_APP_DIR = SETTINGS_DIR.parent
DJANGO_ROOT = CORE_APP_DIR.parent

SECRET_KEY = env('SECRET_KEY')

DATABASES = {'default': dj_database_url.config()}

DEBUG = env.bool('DEBUG', False)

sentry_sdk.init(
    dsn=env.str('SENTRY_URL'),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

COMPRESS_OFFLINE = env.bool('COMPRESS_OFFLINE', default=True)
COMPRESS_ENABLED = env.bool('COMPRESS_ENABLED', default=True)

NODE_MODULES_PATH = Path(DJANGO_ROOT, 'node_modules')

# When we generate css files we ALSO generate prefix (-moz-, -wk-, -ms-)
# In local env we only do "make css" command for performances reasons.
SASS_PATH = 'make fullcss'

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', '{} include={} infile={{infile}} outfile={{outfile}}'.format(
        SASS_PATH, NODE_MODULES_PATH)),
)

STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = [
    Path(DJANGO_ROOT, 'static'),
    Path(DJANGO_ROOT, 'node_modules'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATES = TEMPLATES.copy()
TEMPLATES[0]['DIRS'] = [Path(DJANGO_ROOT, 'templates')]

LOCALE_PATHS = [
    Path(DJANGO_ROOT, 'locales'),
]

cache_config = {
    'default': {
        'BACKEND': env('CACHE_BACKEND', default='django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': env('CACHE_LOCATION', default=''),
    }
}
CACHES.update(cache_config)

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='memory://')

env_allowed_hosts = []
try:
    env_allowed_hosts = env('ALLOWED_HOSTS', default='').split(",")
except KeyError:
    pass

INTERNAL_IPS = env.list('INTERNAL_IPS', default=['127.0.0.1'])

ALLOWED_HOSTS = ["localhost"] + env_allowed_hosts

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_WHITELIST = env.list('EMAIL_WHITELIST', [])

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Emails & Sendinblue api and settings
SIB_API_KEY = env('SIB_API_KEY')
ANYMAIL = {
    'SENDINBLUE_API_KEY': SIB_API_KEY,
}
SIB_EXPORT_CONTACTS_LIST_ID = env.int('SIB_EXPORT_CONTACTS_LIST_ID', 0)
EXPORT_CONTACTS_ENABLED = env.bool('EXPORT_CONTACTS_ENABLED', False)
SIB_WELCOME_EMAIL_TEMPLATE_ID = env.int('SIB_WELCOME_EMAIL_TEMPLATE_ID', 0)
SIB_WELCOME_EMAIL_ENABLED = env.bool('SIB_WELCOME_EMAIL_ENABLED', False)
SIB_PUBLICATION_EMAIL_ENABLED = env.bool('SIB_PUBLICATION_EMAIL_ENABLED', False)
SIB_PUBLICATION_EMAIL_TEMPLATE_ID = env.int('SIB_PUBLICATION_EMAIL_TEMPLATE_ID', 0)
SIB_ALERT_CONFIRMATION_EMAIL_TEMPLATE_ID = env.int('SIB_ALERT_CONFIRMATION_EMAIL_TEMPLATE_ID', 0)
MAILING_LIST_URL = env('MAILING_LIST_URL')
CONTACT_EMAIL = env('CONTACT_EMAIL')
CONTACT_PHONE = env('CONTACT_PHONE')

# Alerts
ALERT_EMAIL_FEEDBACK_FORM_URL = env('ALERT_EMAIL_FEEDBACK_FORM_URL', default='')
ALERT_DELETE_FEEDBACK_FORM_URL = env('ALERT_DELETE_FEEDBACK_FORM_URL', default='')

# File storage settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

# Piwik
ANALYTICS_ENABLED = env.bool('ANALYTICS_ENABLED')
ANALYTICS_SITEID = env('ANALYTICS_SITEID')
GOAL_REGISTER_ID = env.int('GOAL_REGISTER_ID')
GOAL_FIRST_LOGIN_ID = env.int('GOAL_FIRST_LOGIN_ID')


# Minisites
ENABLE_MINISITES_REDIRECTION = env.bool('ENABLE_MINISITES_REDIRECTION', True)

# Hotjar
HOTJAR_SITEID = env('HOTJAR_SITEID')

# Caching
ENABLE_AID_LIST_API_CACHE = env.bool('ENABLE_AID_LIST_API_CACHE', False)
AID_LIST_API_CACHE_TIMEOUT = env.int('AID_LIST_API_CACHE_TIMEOUT', 0)
ENABLE_AID_DETAIL_API_CACHE = env.bool('ENABLE_AID_DETAIL_API_CACHE', False)
AID_DETAIL_API_CACHE_TIMEOUT = env.int('AID_DETAIL_API_CACHE_TIMEOUT', 0)

# Scalingo
SCALINGO_API_TOKEN = env('SCALINGO_API_TOKEN')

# Imports
GRAND_EST_API_USERNAME = env('GRAND_EST_API_USERNAME')
GRAND_EST_API_PASSWORD = env('GRAND_EST_API_PASSWORD')
