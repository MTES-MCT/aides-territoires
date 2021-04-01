"""
WSGI config for minisites on scalingo.
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "minisites.settings.scalingo")

application = Cling(get_wsgi_application())
