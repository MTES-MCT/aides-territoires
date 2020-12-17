# flake8: noqa

from unipath import Path

DEBUG = False

# Absolute filesystem path to the project directory
PROJECT_ROOT = Path(__file__).ancestor(4)

# Absolute path to the Django subdirectory
DJANGO_ROOT = PROJECT_ROOT.child('src')

# Path to the directory where public files will be served
PUBLIC_ROOT = PROJECT_ROOT.child('public')

ALLOWED_HOSTS = []


DJANGO_APPS = [
    'django.forms',  # This is needed because of the custom form renderer
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    'django.contrib.flatpages',
]

THIRD_PARTY_APPS = [
    'compressor',
    'rest_framework',
    'django_xworkflows',
    'corsheaders',
    'actstream',
    'import_export',
    'admin_auto_filters',
    'drf_yasg',
]

LOCAL_APPS = [
    'core',
    'accounts',
    'home',
    'geofr',
    'backers',
    'tags',
    'aids',
    'dataproviders',
    'analytics',
    'data',
    'alerts',
    'bookmarks',
    'programs',
    'categories',
    'search',
    'stats',
    'pages',
    'minisites',
    'logs',
    'upload',
    'exporting',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

VALIDATORS_PATH = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': VALIDATORS_PATH + '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': VALIDATORS_PATH + '.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': VALIDATORS_PATH + '.CommonPasswordValidator',
    },
    {
        'NAME': VALIDATORS_PATH + '.NumericPasswordValidator',
    },
]
AUTH_USER_MODEL = 'accounts.User'


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    DJANGO_ROOT.child('static'),
    DJANGO_ROOT.child('node_modules'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATIC_ROOT = PUBLIC_ROOT.child('static')

MEDIA_URL = '/media/'

MEDIA_ROOT = PUBLIC_ROOT.child('media')

NODE_MODULES_PATH = DJANGO_ROOT.child('node_modules')

SASS_PATH = 'make css'

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', '{} include={} infile={{infile}} outfile={{outfile}}'.format(
        SASS_PATH, NODE_MODULES_PATH)),
)

LOCALE_PATHS = [
    DJANGO_ROOT.child('locales'),
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [DJANGO_ROOT.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.integration',
                'core.context_processors.contact_data',
                'core.context_processors.admin_stats',
                'core.context_processors.contributor_stats',
            ],
            'libraries': {
                'form_utils': 'core.templatetags.form_utils',
            }
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
}

# Bump minor if the modification is retro-compatible, major othewise
CURRENT_API_VERSION = '1.1'

CORS_ALLOW_ALL_ORIGINS = True
CORS_URLS_REGEX = r'^/api/.*$'

# Define a custom logger that sends events to admin users
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'aidesterritoires': {
            'handlers': ['mail'],
            'level': 'INFO',
        }
    }
}

ADMINS = [('Aides-territoires', 'nowhere@example.org')]

MAILING_LIST_URL = None

APPROACHING_DEADLINE_DELTA = 30  # days

UNVALIDATED_ALERTS_QUOTA = 10
MAX_ALERTS_QUOTA = 100

ANALYTICS_ENABLED = False
ANALYTICS_SITEID = 0
HOTJAR_SITEID = 0

CONTACT_EMAIL = 'nowhere@example.org'
CONTACT_PHONE = '+33123456789'
EMAIL_SUBJECT_PREFIX = '[Aides-territoires] '
DEFAULT_FROM_EMAIL = 'aides-territoires@beta.gouv.fr'
SERVER_EMAIL = 'aides-territoires@beta.gouv.fr'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_WHITELIST = []

SITE_ID = 1

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'aid_draft_list_view'

SEARCH_COOKIE_NAME = 'currentsearch'

SIB_API_KEY = ''
SIB_LIST_ID = ''
