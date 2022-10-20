from .base import *  # noqa

DEBUG = False

ENV_NAME = "test"

# Django automatically prepends db name with "test_"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "aides",
        "USER": "aides",
        "PASSWORD": "aides",
        "HOST": "localhost",
    }
}

SECRET_KEY = "Stupid and not very secret key used for tests."

# Makes Celery working synchronously and in memory
CELERY_BROKER_URL = "memory://"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Piwik goal tracking ids
GOAL_REGISTER_ID = 1
GOAL_FIRST_LOGIN_ID = 2

# Speedup user creation
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

ENABLE_MINISITES_REDIRECTION = False
