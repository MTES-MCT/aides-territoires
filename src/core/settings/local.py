import environ

from .base import *  # noqa
from .base import INSTALLED_APPS, MIDDLEWARE, TEMPLATES

DEBUG = True


TEMPLATES[0]['OPTIONS']['debug'] = True
TEMPLATES[0]['OPTIONS']['context_processors'].insert(0, 'django.template.context_processors.debug')

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE


# Create a .env.local file in django's root
environ.Env.read_env('.env.local')
env = environ.Env()

ENV_NAME = 'local'

SECRET_KEY = env('SECRET_KEY', default='hg_1)(oo53y2ow1bvlr6k2mv#hk1lo4%6qf1pdf*02%$203kmt')

DATABASES = {
    'default': env.db(
        default='psql://aidesterritoires:aidesterritoires@localhost/aidesterritoires')
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['.aides-territoires.local'])

INTERNAL_IPS = env.list('INTERNAL_IPS', default=['127.0.0.1'])

COMPRESS_OFFLINE = env.bool('COMPRESS_OFFLINE', False)

MAILING_LIST_URL = env('MAILING_LIST_URL')

ANALYTICS_SITEID = env.int('ANALYTICS_SITEID', 0)

# Celery configuration
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='memory://')
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Piwik goal tracking ids
GOAL_REGISTER_ID = env.int('GOAL_REGISTER_ID', 1)
GOAL_FIRST_LOGIN_ID = env.int('GOAL_FIRST_LOGIN_ID', 2)

EMAIL_BACKEND = env(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend')
EMAIL_WHITELIST = env.list('EMAIL_WHITELIST', [])

# Sendinblue api and settings
SIB_API_KEY = env('SIB_API_KEY')
ANYMAIL = {
    'SENDINBLUE_API_KEY': SIB_API_KEY,
}
SIB_EXPORT_CONTACTS_LIST_ID = env.int('SIB_EXPORT_CONTACTS_LIST_ID', 0)
SIB_WELCOME_EMAIL_ENABLED = env.bool('SIB_WELCOME_EMAIL_ENABLED', False)
SIB_WELCOME_EMAIL_TEMPLATE_ID = env.int('SIB_WELCOME_EMAIL_TEMPLATE_ID', 0)
SIB_PUBLICATION_EMAIL_ENABLED = env.bool('SIB_PUBLICATION_EMAIL_ENABLED', False)
SIB_PUBLICATION_EMAIL_TEMPLATE_ID = env.int('SIB_PUBLICATION_EMAIL_TEMPLATE_ID', 0)

ENABLE_DJANGO_STATIC_SERVE = env.bool('ENABLE_DJANGO_STATIC_SERVE', True)

ENABLE_AID_LIST_API_CACHE = env.bool('ENABLE_AID_LIST_API_CACHE', False)
AID_LIST_API_CACHE_TIMEOUT = env.int('AID_LIST_API_CACHE_TIMEOUT', 0)
ENABLE_AID_DETAIL_API_CACHE = env.bool('ENABLE_AID_DETAIL_API_CACHE', False)
AID_DETAIL_API_CACHE_TIMEOUT = env.int('AID_DETAIL_API_CACHE_TIMEOUT', 0)
