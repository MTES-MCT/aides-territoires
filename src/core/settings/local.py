import environ

from .base import *  # noqa
from .base import INSTALLED_APPS, MIDDLEWARE, TEMPLATES, CACHES

DEBUG = True


TEMPLATES[0]["OPTIONS"]["debug"] = True
TEMPLATES[0]["OPTIONS"]["context_processors"].insert(
    0, "django.template.context_processors.debug"
)

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE


# Create a .env.local file in django's root
environ.Env.read_env(".env.local")
env = environ.Env()

ENV_NAME = "local"

SECRET_KEY = env(
    "SECRET_KEY", default="hg_1)(oo53y2ow1bvlr6k2mv#hk1lo4%6qf1pdf*02%$203kmt"
)

DATABASES = {
    "default": env.db(
        default="psql://aidesterritoires:aidesterritoires@localhost/aidesterritoires"
    )
}

CACHE_BACKEND = env(
    "CACHE_BACKEND", default="django.core.cache.backends.locmem.LocMemCache"
)
CACHE_LOCATION = env("CACHE_LOCATION", default="")
cache_config = {
    "default": {
        "BACKEND": CACHE_BACKEND,
        "LOCATION": CACHE_LOCATION,
    }
}
CACHES.update(cache_config)

# Defender
# Used to limit login attempts
# Only activated if Redis is set
if "redis" in CACHE_BACKEND:
    DEFENDER_REDIS_URL = CACHE_LOCATION
    INSTALLED_APPS += ["defender"]
    MIDDLEWARE += ["defender.middleware.FailedLoginMiddleware"]

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[".aides-territoires.localhost"])

INTERNAL_IPS = env.list("INTERNAL_IPS", default=["127.0.0.1"])

COMPRESS_OFFLINE = env.bool("COMPRESS_OFFLINE", False)

MAILING_LIST_URL = env("MAILING_LIST_URL")

ANALYTICS_SITEID = env.int("ANALYTICS_SITEID", 0)

# Minisites
ENABLE_MINISITES_REDIRECTION = env.bool("ENABLE_MINISITES_REDIRECTION", False)

# Celery configuration
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="memory://")
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Piwik goal tracking ids
GOAL_REGISTER_ID = env.int("GOAL_REGISTER_ID", 1)
GOAL_FIRST_LOGIN_ID = env.int("GOAL_FIRST_LOGIN_ID", 2)

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_WHITELIST = env.list("EMAIL_WHITELIST", [])

# Sendinblue api and settings
SIB_API_KEY = env("SIB_API_KEY")
SIB_CLIENT_KEY = env.str("SIB_CLIENT_KEY", "")
SIB_NEWSLETTER_LIST_IDS = env("SIB_NEWSLETTER_LIST_IDS")
SIB_NEWSLETTER_ID = env("SIB_NEWSLETTER_ID")
ANYMAIL = {
    "SENDINBLUE_API_KEY": SIB_API_KEY,
}
SIB_EXPORT_CONTACTS_LIST_ID = env.int("SIB_EXPORT_CONTACTS_LIST_ID", 0)
SIB_WELCOME_EMAIL_ENABLED = env.bool("SIB_WELCOME_EMAIL_ENABLED", False)
SIB_WELCOME_MIXTE_EMAIL_TEMPLATE_ID = env.int("SIB_WELCOME_MIXTE_EMAIL_TEMPLATE_ID", 0)
SIB_WELCOME_CONTRIBUTOR_EMAIL_TEMPLATE_ID = env.int(
    "SIB_WELCOME_CONTRIBUTOR_EMAIL_TEMPLATE_ID", 0
)
SIB_WELCOME_BENEFICIARY_EMAIL_TEMPLATE_ID = env.int(
    "SIB_WELCOME_BENEFICIARY_EMAIL_TEMPLATE_ID", 0
)
SIB_SUGGESTED_AID_EMAIL_ENABLED = env.bool("SIB_SUGGESTED_AID_EMAIL_ENABLED", False)
SIB_SUGGESTED_AID_ACCEPTED_TEMPLATE_ID = env.int(
    "SIB_SUGGESTED_AID_ACCEPTED_TEMPLATE_ID", 0
)
SIB_SUGGESTED_AID_DENIED_TEMPLATE_ID = env.int(
    "SIB_SUGGESTED_AID_DENIED_TEMPLATE_ID", 0
)
SIB_NEW_SUGGESTED_AID_TEMPLATE_ID = env.int("SIB_NEW_SUGGESTED_AID_TEMPLATE_ID", 0)
SIB_NEW_AID_ASSOCIATED_IN_FAVORITE_PROJECT_TEMPLATE_ID = env.int(
    "SIB_NEW_AID_ASSOCIATED_IN_FAVORITE_PROJECT_TEMPLATE_ID", 0
)
SIB_DELETE_PROJECT_EMAIL_ENABLED = env.bool("SIB_DELETE_PROJECT_EMAIL_ENABLED", False)
SIB_DELETE_PROJECT_EMAIL_TEMPLATE_ID = env.int(
    "SIB_DELETE_PROJECT_EMAIL_TEMPLATE_ID", 0
)
SIB_PUBLICATION_EMAIL_ENABLED = env.bool("SIB_PUBLICATION_EMAIL_ENABLED", False)
SIB_PUBLICATION_EMAIL_TEMPLATE_ID = env.int("SIB_PUBLICATION_EMAIL_TEMPLATE_ID", 0)
SIB_ALERT_CONFIRMATION_EMAIL_TEMPLATE_ID = env.int(
    "SIB_ALERT_CONFIRMATION_EMAIL_TEMPLATE_ID", 0
)
SIB_NEWSLETTER_CONFIRM_TEMPLATE_ID = env.int("SIB_NEWSLETTER_CONFIRM_TEMPLATE_ID", 0)

ENABLE_DJANGO_STATIC_SERVE = env.bool("ENABLE_DJANGO_STATIC_SERVE", True)

# Matomo
MATOMO_SITE_ID = env.int("MATOMO_SITE_ID", 0)

# Caching
ENABLE_AID_LIST_API_CACHE = env.bool("ENABLE_AID_LIST_API_CACHE", False)
AID_LIST_API_CACHE_TIMEOUT = env.int("AID_LIST_API_CACHE_TIMEOUT", 0)
ENABLE_AID_DETAIL_API_CACHE = env.bool("ENABLE_AID_DETAIL_API_CACHE", False)
AID_DETAIL_API_CACHE_TIMEOUT = env.int("AID_DETAIL_API_CACHE_TIMEOUT", 0)
ENABLE_OTHER_LIST_API_CACHE = env.bool("ENABLE_OTHER_LIST_API_CACHE", False)
OTHER_LIST_API_CACHE_TIMEOUT = env.int("OTHER_LIST_API_CACHE_TIMEOUT", 0)
ENABLE_OTHER_DETAIL_API_CACHE = env.bool("ENABLE_OTHER_DETAIL_API_CACHE", False)
OTHER_DETAIL_API_CACHE_TIMEOUT = env.int("OTHER_DETAIL_API_CACHE_TIMEOUT", 0)

# Scalingo
SCALINGO_API_TOKEN = env("SCALINGO_API_TOKEN", default="")

# Admin
ADMIN_OTP_ENABLED = env.bool("ADMIN_OTP_ENABLED", False)

# File storage settings
DEFAULT_FILE_STORAGE = env(
    "DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default="")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="")
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False

"""
Adding a second template just for the django_debug_toolbar which requires:
- "APP_DIRS": True
- which is incompatible with "loaders", so it is removed here
- (and "loader" itself is mandatory for django-admin-tools)
"""
TEMPLATES += [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "NAME": "For django_debug_toolbar",
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": True,
            "context_processors": [
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.integration",
                "core.context_processors.contact_data",
                "core.context_processors.admin_stats",
                "core.context_processors.contributor_stats",
            ],
            "libraries": {
                "form_utils": "core.templatetags.form_utils",
            },
        },
    }
]

ADEME_AGIR_API_USERNAME = env("ADEME_AGIR_API_USERNAME", default="")
ADEME_AGIR_API_PASSWORD = env("ADEME_AGIR_API_PASSWORD", default="")
