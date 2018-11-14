from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    tag = models.CharField(
        _('Tag'),
        max_length=50,
        unique=True,
        db_index=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
