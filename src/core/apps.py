from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = "core"

    def ready(self):
        # Celery :
        # This will make sure the app is always imported when
        # Django starts so that shared_task will use this app.
        from core.celery import app as celery_app  # noqa

        __all__ = ("celery_app",)  # noqa
