from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.indexes import GinIndex


class Tag(models.Model):
    name = models.CharField(_("Name"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        indexes = [
            GinIndex(name="tag_name_trgm", fields=["name"], opclasses=["gin_trgm_ops"]),
        ]

    def __str__(self):
        return self.name
