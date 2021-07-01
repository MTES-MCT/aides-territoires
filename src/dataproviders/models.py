from django.db import models
from django.utils import timezone

from dataproviders.constants import IMPORT_LICENCES


class DataSource(models.Model):
    name = models.CharField(
        'Nom',
        max_length=256)
    description = models.TextField(
        'Description complète de la source de données',
        blank=True)
    import_details = models.TextField(
        "Détails additionels concernant l'import",
        blank=True)

    backer = models.ForeignKey(
        'backers.Backer',
        verbose_name="Porteur d'aides",
        on_delete=models.PROTECT,
        null=True, blank=True)
    perimeter = models.ForeignKey(
        'geofr.Perimeter',
        verbose_name='Périmètre',
        on_delete=models.PROTECT,
        null=True, blank=True)

    import_api_url = models.URLField(
        "URL de l'API",
        help_text="L'URL utilisée par le script d'import",
        null=True, blank=True)
    import_data_url = models.URLField(
        "URL d'origine de la donnée importée",
        null=True, blank=True)
    import_licence = models.CharField(
        "Sous quelle licence cette source a-t-elle été importée ?",
        max_length=50,
        choices=IMPORT_LICENCES,
        blank=True)

    contact_team = models.ForeignKey(
        'accounts.User',
        verbose_name='Contact (team AT)',
        on_delete=models.PROTECT,
        related_name='import_contact_team',
        limit_choices_to={'is_superuser': True},
        null=True)
    contact_backer = models.TextField(
        'Contact(s) coté porteur',
        blank=True)
    aid_author = models.ForeignKey(
        'accounts.User',
        verbose_name="L'auteur par défaut des aides importées",
        on_delete=models.PROTECT,
        related_name='import_aid_author',
        help_text='Mettre Admin AT par défaut',
        null=True)

    date_created = models.DateTimeField(
        'Date de création',
        default=timezone.now)
    date_updated = models.DateTimeField(
        'Date de mise à jour',
        auto_now=True)
    date_last_access = models.DateField(
        'Date du dernier accès',
        null=True, blank=True)

    class Meta:
        verbose_name = 'Source de données'
        verbose_name_plural = 'Sources de données'

    def __str__(self):
        return self.name
