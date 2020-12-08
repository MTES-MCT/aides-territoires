from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ExportingConfig(AppConfig):
    name = 'exporting'
    verbose_name = _('data export')
