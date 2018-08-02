from .base import *  # noqa
from .base import DJANGO_ROOT

DEBUG = True

SECRET_KEY = 'hg_1)(oo53y2ow1bvlr6k2mv#hk1lo4%6qf1pdf*02%$203kmt'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [DJANGO_ROOT.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
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

ALLOWED_HOSTS = ['aides-territoires.local']
