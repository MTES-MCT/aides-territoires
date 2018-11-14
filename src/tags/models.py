from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=50,
        unique=True)
    slug = models.SlugField(
        _('Slug'),
        max_length=50,
        unique=True,
        db_index=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
