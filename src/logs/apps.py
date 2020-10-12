from django.apps import AppConfig
from django.apps import apps
from django.utils.translation import ugettext_lazy as _


class LogsConfig(AppConfig):
    name = 'logs'
    verbose_name = _('logs')

    def ready(self):
        # Activity stream registration
        from actstream import registry
        registry.register(apps.get_model('alerts.Alert'))
