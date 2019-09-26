from django.db import models
from django.utils.translation import ugettext_lazy as _


class Program(models.Model):
    """Represents a single aid program.

    Real-life examples of such programs:
      - Territoires d'Industrie
      - Action Cœur de Ville

    Aid programs regroup new or existing aids, and generally
    are limited to a specific perimeter.
    """

    name = models.CharField(
        _('Name'),
        max_length=256)
    aids = models.ManyToManyField(
        'aids.Aid',
        verbose_name=_('Aids'))
    perimeter = models.ForeignKey(
        'geofr.Perimeter',
        on_delete=models.PROTECT,
        verbose_name=_('Perimeter'))

    class Meta:
        verbose_name = _('Aid program')
        verbose_name_plural = _('Aid programs')
