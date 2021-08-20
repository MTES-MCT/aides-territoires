from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings

from core.fields import ChoiceArrayField
from model_utils import Choices
from aids.constants import AUDIENCES_ALL


class Organization(models.Model):

    ORGANIZATION_TYPE = Choices(*AUDIENCES_ALL)

    name = models.CharField(
        'Nom',
        max_length=256,
        db_index=True)
    slug = models.SlugField(
        "Fragment d'URL",
        help_text='Laisser vide pour autoremplir.',
        blank=True)
    organization_type = ChoiceArrayField(
        verbose_name="Type de structure",
        null=True, blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=ORGANIZATION_TYPE))
    beneficiaries = models.ManyToManyField(
        'accounts.User',
        verbose_name='Bénéficiaires',
        blank=True)
    projects = models.ManyToManyField(
        'projects.Project',
        verbose_name='Projets',
        blank=True)
    perimeter = models.ForeignKey(
        'geofr.Perimeter',
        verbose_name="Périmètre de la structure",
        on_delete=models.PROTECT,
        help_text="Sur quel périmètre la structure intervient-elle ?",
        null=True, blank=True)

    date_created = models.DateTimeField(
        'Date de création',
        default=timezone.now)
    date_updated = models.DateTimeField(
        'Date de mise à jour',
        auto_now=True)

    class Meta:
        verbose_name = 'Structure'
        verbose_name_plural = 'Structures'

    def __str__(self):
        return self.name

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)
