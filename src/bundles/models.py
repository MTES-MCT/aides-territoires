from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Bundle(models.Model):
    """Represents a selected list of aids.

    `List` would be an appropriate name for this class, if it was not a
    Python reserved word.
    """

    slug = models.SlugField(
        _('Slug'),
        help_text=_('Let it empty so it will be autopopulated.'),
        blank=True)
    owner = models.ForeignKey(
        'accounts.User',
        verbose_name=_('Owner'),
        on_delete=models.PROTECT,
        related_name='bundles')
    name = models.CharField(
        max_length=64,
        verbose_name=_('Bundle name'),
        blank=False)
    aids = models.ManyToManyField(
        'aids.Aid',
        verbose_name=_('Aids'),
        related_name='bundles')

    class Meta:
        verbose_name = _('Bundle')
        verbose_name_plural = _('Bundles')

    def save(self, *args, **kwargs):
        """Populate the slug field.

        Let's make sure lists have unique names, by prefixing random
        characters.
        """
        if not self.id or self.slug == '':
            full_title = '{}-{}'.format(str(uuid4())[:4], self.name)
            self.slug = slugify(full_title)[:50]
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
