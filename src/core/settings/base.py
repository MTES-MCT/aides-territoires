# flake8: noqa
from unipath import Path

from core.api import doc as api_doc


DEBUG = False

# Absolute filesystem path to the project directory
PROJECT_ROOT = Path(__file__).ancestor(4)

# Absolute path to the Django subdirectory
DJANGO_ROOT = PROJECT_ROOT.child('src')

# Path to the directory where public files will be served
PUBLIC_ROOT = PROJECT_ROOT.child('public')

ALLOWED_HOSTS = []


DJANGO_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
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
    'django.contrib.sitemaps',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'compressor',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'django_xworkflows',
    'corsheaders',
    'import_export',
    'admin_auto_filters',
    'anymail',
    'django_celery_beat',
    'adminsortable2',
    'fieldsets_with_inlines',
    'django_otp',
    'django_otp.plugins.otp_totp',
]

LOCAL_APPS = [
    'core',
    'accounts',
    'home',
    'geofr',
    'backers',
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
    'upload',
    'exporting',
    'emails',
    'projects',
    'blog',
    'eligibility',
    'admin_lite',
    'organizations',

    # deprecated apps
    'tags',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

# Models

AUTH_USER_MODEL = 'accounts.User'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


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
        'NAME': 'BASE',
        'DIRS': [DJANGO_ROOT.child('templates')],
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
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader',
            ],
            'libraries': {
                'form_utils': 'core.templatetags.form_utils',
            }
        },
    },
]


ADMIN_TOOLS_THEMING_CSS = 'css/theming.css'
ADMIN_TOOLS_MENU = 'core.admin_menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'core.admin_dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'core.admin_dashboard.CustomAppIndexDashboard'

ADMIN_OTP_ENABLED = False
OTP_TOTP_ISSUER = "Aides-territoires"


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Bump minor if the modification is retro-compatible, major othewise
CURRENT_API_VERSION = '1.4'

# The file path that's user for storing the json dump on S3
ALL_AIDS_DUMP_FILE_PATH = 'aids/all-aids.json'

# Swagger / Redoc settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Aides-territoires API',
    'VERSION': CURRENT_API_VERSION,
    'DESCRIPTION': api_doc.description,
    'TOS': 'https://aides-territoires.beta.gouv.fr/mentions-l%C3%A9gales/',
    'CONTACT': {
        'name': "Une question ? Vous pouvez nous contacter en cliquand ici (puis sélectionnez 'API' comme Sujet)",
        'url': 'https://aides-territoires.beta.gouv.fr/contact/'
    },
    'LICENSE': {
        'name': "« Licence Ouverte v2.0 » d'Etalab"
    },
    'EXTERNAL_DOCS': {
        'url': 'https://aides-territoires.beta.gouv.fr/data/'
    },
    'SERVE_INCLUDE_SCHEMA': False,
    'SORT_OPERATION_PARAMETERS': False
}

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

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

ADMINS = [('Aides-territoires', 'nowhere@example.org')]

MAILING_LIST_URL = None

APPROACHING_DEADLINE_DELTA = 30  # days

ANALYTICS_ENABLED = False
ANALYTICS_ENDPOINT = 'https://stats.data.gouv.fr/index.php'
ANALYTICS_SITEID = 0
HOTJAR_SITEID = 0

# Emails & Sendinblue api and settings
CONTACT_EMAIL = 'nowhere@example.org'
CONTACT_PHONE = '+33123456789'
EMAIL_SUBJECT_PREFIX = '[Aides-territoires] '
DEFAULT_FROM_EMAIL = 'Aides-territoires <aides-territoires@beta.gouv.fr>'
SERVER_EMAIL = 'aides-territoires@beta.gouv.fr'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_WHITELIST = []
SIB_API_KEY = ''
SIB_NEWSLETTER_LIST_IDS = []
SIB_NEWSLETTER_ID = []
SIB_EXPORT_CONTACTS_LIST_ID = 0
SIB_WELCOME_EMAIL_ENABLED = False
SIB_WELCOME_EMAIL_TEMPLATE_ID = 0
SIB_PUBLICATION_EMAIL_ENABLED = False
SIB_PUBLICATION_EMAIL_TEMPLATE_ID = 0
SIB_ALERT_CONFIRMATION_EMAIL_TEMPLATE_ID = 0
SIB_NEWSLETTER_CONFIRM_TEMPLATE_ID = 0
EXPORT_CONTACTS_ENABLED = False

# Matomo
MATOMO_SITE_ID = 0

# Alerts
UNVALIDATED_ALERTS_QUOTA = 10
MAX_ALERTS_QUOTA = 100
ALERT_EMAIL_FEEDBACK_FORM_URL = ''  # form in the alert email
ALERT_DELETE_FEEDBACK_FORM_URL = ''  # form after the alert deletion

# Minisites detection:
# This is a mapping between a DNS host and a minisite slug.
# Sometimes, a minisite can be served under a custom domain.
# If that context, we use this mapping in order to identify
# which ministe the custom domain should be linked to.
MAP_DNS_TO_MINISITES = [
    ('aides.francemobilites.fr', 'francemobilites'),
]

# Minisite redirection:
# Sometime, we want to redirect the minisites URL.
# If redirection is enabled, we first check if an external DNS such as
# `aides.francemobilites.fr` is defined. If so, that DNS will be used.
# Otherwise, the redireciton will target the subdmain  URL, for instance
# `https://renovation-energetique.aides-territoires.beta.gouv.fr/`
ENABLE_MINISITES_REDIRECTION = True
REDIRECT_MINISITES_TO_EXTERNAL_URL = [
    ('francemobilites', 'https://aides.francemobilites.fr'),
    ('france-relance-cvl', 'https://centre-val-de-loire.aides-territoires.beta.gouv.fr'),
]

# ADDNA
ADDNA_ALERT_TITLE = 'Développement Durable - Nouvelle-Aquitaine - ADDNA'
ADDNA_ALERT_QUERYSTRING = 'perimeter=70971-nouvelle-aquitaine'
ADDNA_ALERT_EMAIL_SUBJECT_PREFIX = '[Aides-territoires-ADDNA] '

SITE_ID = 1

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'user_dashboard'

SEARCH_COOKIE_NAME = 'currentsearch'

ENABLE_DJANGO_STATIC_SERVE = False

# Caching
ENABLE_AID_LIST_API_CACHE = False
AID_LIST_API_CACHE_TIMEOUT = 0
ENABLE_AID_DETAIL_API_CACHE = False
AID_DETAIL_API_CACHE_TIMEOUT = 0

# Scalingo
SCALINGO_API_TOKEN = ''

# Imports
GRAND_EST_API_USERNAME = ''
GRAND_EST_API_PASSWORD = ''
