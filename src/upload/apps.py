from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UploadConfig(AppConfig):
    name = "upload"
    verbose_name = _("upload")
