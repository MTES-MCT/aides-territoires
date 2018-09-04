from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from model_utils import Choices


class Perimeter(models.Model):
    """Represents a single application perimeter for an Aid."""

    TYPES = Choices(
        (1, 'commune', _('Commune')),
        (2, 'epci', _('EPCI')),
        (3, 'department', _('Department')),
        (4, 'region', _('Region')),
        (5, 'cluster', _('Cluster')),  # Group of regions
        (6, 'country', _('Country')),
        (7, 'continent', _('Continent')),
    )

    scale = models.PositiveIntegerField(
        _('Scale'),
        choices=TYPES)
    code = models.CharField(
        _('Code'),
        max_length=16)
    name = models.CharField(
        _('Name'),
        max_length=128)

    region = models.CharField(
        _('Region'),
        max_length=2,
        blank=True)
    department = models.CharField(
        _('Departments'),
        max_length=3,
        blank=True)
    epci = models.CharField(
        _('EPCI'),
        max_length=32,
        blank=True)
    commune = models.CharField(
        _('Commune'),
        max_length=32,
        blank=True)
    zipcodes = ArrayField(
        verbose_name=_('Zip codes'),
        base_field=models.CharField(max_length=8),
        null=True, blank=True)

    class Meta:
        verbose_name = _('Perimeter')
        verbose_name_plural = _('Perimeters')
        unique_together = (
            ('scale', 'code'),
        )
