from .base import *  # noqa
from .base import DJANGO_ROOT

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


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [DJANGO_ROOT.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'form_utils': 'core.templatetags.form_utils',
            }
        },
    },
]

SECRET_KEY = 'Stupid and not very secret key used for tests.'
