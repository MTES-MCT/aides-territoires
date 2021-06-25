from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex

from model_utils import Choices

from core.utils import remove_accents


class Perimeter(models.Model):
    """Represents a single application perimeter for an Aid.

    Each perimeter represents a location (e.g a region, a department, a
    commune…) and contains data about where it is located.

    E.g: the commune of Montpellier is located in Hérault, Occitanie, France,
    Europe.

    Since nothing is simple when administration is involved, some perimeters
    e.g epcis can be spread over several departments / regions.

    Drainage basins are another edge case, since they are independant from any
    existing legal borders.
    https://fr.wikipedia.org/wiki/Bassin_hydrographique

    """

    TYPES = Choices(
        (1, 'commune', 'Commune'),
        (5, 'epci', 'EPCI'),
        (8, 'basin', 'Bassin hydrographique'),
        (10, 'department', 'Département'),
        (15, 'region', 'Région'),
        (16, 'overseas', 'Outre-mer'),
        (17, 'mainland', 'Métropole'),
        (18, 'adhoc', 'Ad-hoc'),
        (20, 'country', 'Pays'),
        (25, 'continent', 'Continent'),
    )

    scale = models.PositiveIntegerField(
        _('Scale'),
        choices=TYPES)
    name = models.CharField(
        _('Name'),
        max_length=128)
    code = models.CharField(
        _('Code'),
        max_length=16,
        help_text=_('Internal usage only, not relevant for Ad-hoc perimeters'))

    contained_in = models.ManyToManyField(
        'geofr.Perimeter',
        verbose_name=_('Contained in'),
        related_name='contains',
        blank=True)
    manually_created = models.BooleanField(
        _('Manually created'),
        default=False)
    is_visible_to_users = models.BooleanField(
        _('The perimeter is visible to users'),
        default=True)

    continent = models.CharField(
        _('Continent'),
        max_length=2,
        default='EU')
    country = models.CharField(
        'Pays',
        max_length=3,
        default='FRA')  # ISO_3166-3 codes
    regions = ArrayField(  # Array of region codes (INSEE COG)
        verbose_name='Régions',
        base_field=models.CharField(max_length=2),
        default=list,
        blank=True)
    departments = ArrayField(  # Array of depts codes (INSEE COG)
        verbose_name='Départements',
        base_field=models.CharField(max_length=3),
        default=list,
        blank=True)
    epci = models.CharField(
        _('EPCI'),
        max_length=32,  # INSEE COG
        blank=True)
    basin = models.CharField(
        _('Drainage basin'),
        max_length=32,  # Sandre code
        blank=True)
    zipcodes = ArrayField(
        verbose_name=_('Zip codes'),
        base_field=models.CharField(max_length=8),
        null=True, blank=True)
    is_overseas = models.BooleanField(
        verbose_name=_('Is overseas?'),
        null=True)

    # This field is used to store the name without accent, for indexing.
    # We recently updated the perimeter search to ignore accents, and at first
    # we were using postgres' unaccent extension.
    # We ran into an issue where the trigram index was not being used anymore
    # bumping the querytime from a few ms to more than 300ms.
    # Since it's kinda hard to add an index on an unaccent expression, it's
    # just easier to store an index the unaccented version of the name.
    unaccented_name = models.CharField(
        _('Name without accent (for indexing purpose)'),
        max_length=128)

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)
    date_updated = models.DateTimeField(
        _('Date updated'),
        auto_now=True)

    class Meta:
        verbose_name = _('Perimeter')
        verbose_name_plural = _('Perimeters')
        unique_together = (
            ('scale', 'code'),
        )
        indexes = [
            GinIndex(
                name='name_trgm',
                fields=['name'],
                opclasses=['gin_trgm_ops']),
            GinIndex(
                name='unaccented_name_trgm',
                fields=['unaccented_name'],
                opclasses=['gin_trgm_ops']),
        ]

    def __str__(self):
        if not self.scale:
            return ''

        if self.scale == self.TYPES.commune and self.zipcodes:
            _str = '{} ({} – {})'.format(
                self.name, self.get_scale_display(), ', '.join(self.zipcodes))
        elif self.scale <= self.TYPES.region:
            _str = '{} ({})'.format(self.name, self.get_scale_display())
        else:
            _str = self.name

        return _str

    @property
    def id_slug(self):
        return '{}-{}'.format(self.id, slugify(self.name))

    def save(self, *args, **kwargs):
        self.unaccented_name = remove_accents(self.name)
        return super().save(*args, **kwargs)
