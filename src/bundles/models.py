from django.db import models
from django.utils.translation import ugettext_lazy as _


class Bundle(models.Model):
    """Represents a selected list of aids.

    `List` would be an appropriate name for this class, if it was not a
    Python reserved word.
    """

    owner = models.ForeignKey(
        'accounts.User',
        verbose_name=_('Owner'),
        on_delete=models.PROTECT)
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

    def __str__(self):
        return self.name