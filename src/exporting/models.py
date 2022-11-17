from django.db import models
from django.utils.translation import gettext_lazy as _


class DataExport(models.Model):
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
        limit_choices_to={"is_superuser": True},
        help_text=_("The person who has trigger the export"),
    )
    exported_file = models.FileField(_("exported file"), upload_to="data-export")
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Data export")
        verbose_name_plural = _("Data export")

    def __str__(self):
        return self.exported_file.name
