import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.production")

from django.conf import settings  # noqa


app = Celery("aides")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def celery_debug_task(self):
    print("This is a debug task to verify that Celery works")
