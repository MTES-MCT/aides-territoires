from .base import *  # noqa

DEBUG = False

# Django automatically prepends db name with "test_"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aides',
        'USER': 'aides',
        'PASSWORD': 'aides',
        'HOST': 'localhost',
        'PORT': '',
    }
}

SECRET_KEY = 'Stupid and not very secret key used for tests.'

# Makes Celery working synchronously and in memory
CELERY_BROKER_URL = "memory://"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
