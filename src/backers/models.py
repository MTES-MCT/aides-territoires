from django.db import models
from django.utils.translation import ugettext_lazy as _


class Backer(models.Model):
    """Represents an entity that backs aids."""

    name = models.CharField(
        _('Name'),
        max_length=256)

    class Meta:
        verbose_name = _('Backer')
        verbose_name_plural = _('Backers')
