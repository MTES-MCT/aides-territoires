from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.indexes import GinTrigramIndex


class Tag(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=50,
        unique=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        indexes = [
            GinTrigramIndex(fields=['name']),
        ]

    def __str__(self):
        return self.name
