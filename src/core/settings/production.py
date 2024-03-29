import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa
from .base import CACHES


COMPRESS_OFFLINE = True

# Create a .env.production file in django's root
environ.Env.read_env(".env.production")
env = environ.Env()

ENV_NAME = env("ENV_NAME")

SECRET_KEY = env("SECRET_KEY")

DATABASES = {"default": env.db()}

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
# Only activated if the Redis cache is set
if "redis" in CACHE_BACKEND:
    DEFENDER_REDIS_URL = CACHE_LOCATION
    INSTALLED_APPS += ["defender"]  # noqa
    MIDDLEWARE += ["defender.middleware.FailedLoginMiddleware"]  # noqa

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INTERNAL_IPS = env.list("INTERNAL_IPS")

CELERY_BROKER_URL = env("CELERY_BROKER_URL")

sentry_sdk.init(
    dsn=env.str("SENTRY_URL"),
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # To set a uniform sample rate
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", 1.0),
)

MAILING_LIST_URL = env("MAILING_LIST_URL")

ANALYTICS_ENABLED = env.bool("ANALYTICS_ENABLED")

ANALYTICS_SITEID = env("ANALYTICS_SITEID")

CONTACT_EMAIL = env("CONTACT_EMAIL")
CONTACT_PHONE = env("CONTACT_PHONE")

ADMINS = [x.split(":") for x in env.list("ADMINS")]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Piwik goal tracking ids
GOAL_REGISTER_ID = env.int("GOAL_REGISTER_ID")
GOAL_FIRST_LOGIN_ID = env.int("GOAL_FIRST_LOGIN_ID")

# When we generate css files we ALSO generate prefix (-moz-, -wk-, -ms-)
# In local env we only do "make css" command for performances reasons.
SASS_PATH = "make fullcss"

EMAIL_BACKEND = env("EMAIL_BACKEND")

# For staging, we want to restrict email sending to a whitelist
EMAIL_WHITELIST = env.list("EMAIL_WHITELIST", [])

# Brevo API and settings
SIB_API_KEY = env("SIB_API_KEY")
SIB_CLIENT_KEY = env.str("SIB_CLIENT_KEY", "")
SIB_NEWSLETTER_LIST_IDS = env("SIB_NEWSLETTER_LIST_IDS")
SIB_NEWSLETTER_ID = env("SIB_NEWSLETTER_ID")
ANYMAIL = {
    "SENDINBLUE_API_KEY": SIB_API_KEY,
}
SIB_EXPORT_CONTACTS_LIST_ID = env.int("SIB_EXPORT_CONTACTS_LIST_ID")
SIB_WELCOME_EMAIL_ENABLED = env.bool("SIB_WELCOME_EMAIL_ENABLED")
SIB_WELCOME_MIXTE_EMAIL_TEMPLATE_ID = env.int("SIB_WELCOME_MIXTE_EMAIL_TEMPLATE_ID")
SIB_WELCOME_CONTRIBUTOR_EMAIL_TEMPLATE_ID = env.int(
    "SIB_WELCOME_CONTRIBUTOR_EMAIL_TEMPLATE_ID"
)
SIB_WELCOME_BENEFICIARY_EMAIL_TEMPLATE_ID = env.int(
    "SIB_WELCOME_BENEFICIARY_EMAIL_TEMPLATE_ID"
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
SIB_DELETE_PROJECT_EMAIL_ENABLED = env.bool("SIB_DELETE_PROJECT_EMAIL_ENABLED")
SIB_DELETE_PROJECT_EMAIL_TEMPLATE_ID = env.int("SIB_DELETE_PROJECT_EMAIL_TEMPLATE_ID")
SIB_PUBLICATION_EMAIL_ENABLED = env.bool("SIB_PUBLICATION_EMAIL_ENABLED")
SIB_PUBLICATION_EMAIL_TEMPLATE_ID = env.int("SIB_PUBLICATION_EMAIL_TEMPLATE_ID")
SIB_ALERT_CONFIRMATION_EMAIL_TEMPLATE_ID = env.int(
    "SIB_ALERT_CONFIRMATION_EMAIL_TEMPLATE_ID"
)
SIB_NEWSLETTER_CONFIRM_TEMPLATE_ID = env.int("SIB_NEWSLETTER_CONFIRM_TEMPLATE_ID", 0)

EXPORT_CONTACTS_ENABLED = env.bool("EXPORT_CONTACTS_ENABLED")

# Matomo
MATOMO_SITE_ID = env("MATOMO_SITE_ID")

# File storage settings
STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False

ENABLE_AID_LIST_API_CACHE = env.bool("ENABLE_AID_LIST_API_CACHE", False)
AID_LIST_API_CACHE_TIMEOUT = env.int("AID_LIST_API_CACHE_TIMEOUT", 0)
ENABLE_AID_DETAIL_API_CACHE = env.bool("ENABLE_AID_DETAIL_API_CACHE", False)
AID_DETAIL_API_CACHE_TIMEOUT = env.int("AID_DETAIL_API_CACHE_TIMEOUT", 0)
ENABLE_OTHER_LIST_API_CACHE = env.bool("ENABLE_OTHER_LIST_API_CACHE", False)
OTHER_LIST_API_CACHE_TIMEOUT = env.int("OTHER_LIST_API_CACHE_TIMEOUT", 0)
ENABLE_OTHER_DETAIL_API_CACHE = env.bool("ENABLE_OTHER_DETAIL_API_CACHE", False)
OTHER_DETAIL_API_CACHE_TIMEOUT = env.int("OTHER_DETAIL_API_CACHE_TIMEOUT", 0)

ADEME_AGIR_API_USERNAME = env("ADEME_AGIR_API_USERNAME", default="")
ADEME_AGIR_API_PASSWORD = env("ADEME_AGIR_API_PASSWORD", default="")
MANCHE_API_USERNAME = env("MANCHE_API_USERNAME", default="")
MANCHE_API_PASSWORD = env("MANCHE_API_PASSWORD", default="")
