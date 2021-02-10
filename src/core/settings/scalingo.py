from pathlib import Path

import dj_database_url
import environ

from .base import *  # noqa
from .base import INSTALLED_APPS, TEMPLATES


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

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

RAVEN_CONFIG = {
    'dsn': env('RAVEN_URL'),
}

COMPRESS_OFFLINE = env.bool('COMPRESS_OFFLINE', default=False)
COMPRESS_ENABLED = env.bool('COMPRESS_ENABLED', default=True)

NODE_MODULES_PATH = Path(DJANGO_ROOT, 'node_modules')

SASS_PATH = 'make css'

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', '{} include={} infile={{infile}} outfile={{outfile}}'.format(
        SASS_PATH, NODE_MODULES_PATH)),
)

STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = [
    Path(DJANGO_ROOT, 'static'),
    Path(DJANGO_ROOT, 'node_modules'),
]

MEDIA_URL = env('MEDIA_URL', default='')

MEDIA_ROOT = env('MEDIA_ROOT', default='')

TEMPLATES = TEMPLATES.copy()
TEMPLATES[0]['DIRS'] = [Path(DJANGO_ROOT, 'templates')]

LOCALE_PATHS = [
    Path(DJANGO_ROOT, 'locales'),
]

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='memory://')
CELERY_TASK_ALWAYS_EAGER = env('CELERY_TASK_ALWAYS_EAGER', default=True)
CELERY_TASK_EAGER_PROPAGATES = env('CELERY_TASK_EAGER_PROPAGATES', default=True)

env_allowed_hosts = []
try:
    env_allowed_hosts = env('ALLOWED_HOSTS', default='').split(",")
except KeyError:
    pass

INTERNAL_IPS = env.list('INTERNAL_IPS', default=['127.0.0.1'])

ALLOWED_HOSTS = ["localhost"] + env_allowed_hosts

MAILING_LIST_URL = env('MAILING_LIST_URL', default='')

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_FILE_PATH = '/tmp/django_emails'

EMAIL_WHITELIST = env.list('EMAIL_WHITELIST', [])
ENABLE_EMAIL_WHITELIST = env.bool('ENABLE_EMAIL_WHITELIST', False)

# Sendinblue api and settings
SIB_API_KEY = env('SIB_API_KEY')
SIB_LIST_ID = env.int('SIB_LIST_ID')
ANYMAIL = {
    'SENDINBLUE_API_KEY': SIB_API_KEY,
}
SIB_WELCOME_EMAIL_TEMPLATE_ID = env.int('SIB_WELCOME_EMAIL_TEMPLATE_ID', 41)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Piwik goal tracking ids
GOAL_REGISTER_ID = env.int('GOAL_REGISTER_ID', 1)
GOAL_FIRST_LOGIN_ID = env.int('GOAL_FIRST_LOGIN_ID', 2)
