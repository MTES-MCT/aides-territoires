from .base import *  # noqa

DEBUG = False

# Django automatically prepends db name with "test_"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aidesterritoires',
        'USER': 'aidesterritoires',
        'PASSWORD': 'aidesterritoires',
        'HOST': 'localhost',
        'PORT': '',
    }
}

SECRET_KEY = 'Stupid and not very secret key used for tests.'
