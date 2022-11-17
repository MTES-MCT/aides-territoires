from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExportingConfig(AppConfig):
    name = "exporting"
    verbose_name = _("data export")
