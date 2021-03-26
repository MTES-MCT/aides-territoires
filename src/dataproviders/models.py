from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from dataproviders.constants import FREQUENCIES, IMPORT_LICENCES


class DataSource(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=256)
    description = models.TextField(
        _('Full description of the data source'),
        blank=True)

    backer = models.ForeignKey(
        'backers.Backer',
        verbose_name=_('Backer'),
        on_delete=models.PROTECT,
        null=True, blank=True)
    perimeter = models.ForeignKey(
        'geofr.Perimeter',
        verbose_name=_('Perimeter'),
        on_delete=models.PROTECT,
        null=True, blank=True)

    import_api_url = models.URLField(
        _('API url of the imported data'),
        null=True, blank=True)
    import_data_url = models.URLField(
        _('Origin url of the imported data'),
        null=True, blank=True)
    import_frequency = models.CharField(
        max_length=32,
        choices=FREQUENCIES,
        default=FREQUENCIES.once)
    import_licence = models.CharField(
        _('Under which license was this source imported?'),
        max_length=50,
        choices=IMPORT_LICENCES,
        blank=True)

    contact_team = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        limit_choices_to={'is_superuser': True},
        verbose_name=_('Contact AT team'),
        null=True)
    contact_backer = models.TextField(
        _('Contact backer'),
        blank=True)

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)
    date_updated = models.DateTimeField(
        _('Date updated'),
        auto_now=True)
    date_last_access = models.DateField(
        _('Date of the latest access'),
        null=True, blank=True)

    class Meta:
        verbose_name = _('Data Source')
        verbose_name_plural = _('Data Sources')

    def __str__(self):
        return self.name
