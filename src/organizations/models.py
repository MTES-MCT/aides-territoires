from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from core.fields import ChoiceArrayField
from model_utils import Choices
from aids.constants import AUDIENCES_ALL
from geofr.models import Perimeter
from geofr.utils import get_all_related_perimeters


class Organization(models.Model):

    ORGANIZATION_TYPE = Choices(*AUDIENCES_ALL)

    name = models.CharField("Nom", max_length=256, db_index=True)
    slug = models.SlugField(
        "Fragment d'URL", help_text="Laisser vide pour autoremplir.", blank=True
    )
    organization_type = ChoiceArrayField(
        verbose_name="Type de structure",
        null=True,
        blank=True,
        base_field=models.CharField(max_length=32, choices=ORGANIZATION_TYPE),
    )
    address = models.CharField("Adresse postale", max_length=900, null=True, blank=True)
    city_name = models.CharField(
        "Nom de la ville", max_length=256, null=True, blank=True
    )
    zip_code = models.PositiveIntegerField("Code postal", null=True, blank=True)

    siren_code = models.BigIntegerField("Code SIREN", null=True, blank=True)
    siret_code = models.BigIntegerField("Code SIRET", null=True, blank=True)
    ape_code = models.CharField("Code APE", max_length=5, null=True, blank=True)

    inhabitants_number = models.PositiveIntegerField(
        "Nombre d'habitants", null=True, blank=True
    )
    voters_number = models.PositiveIntegerField(
        "Nombre de votants", null=True, blank=True
    )
    corporates_number = models.PositiveIntegerField(
        "Nombre d'entreprises", null=True, blank=True
    )
    associations_number = models.PositiveIntegerField(
        "Nombre d'associations", null=True, blank=True
    )

    municipal_roads = models.PositiveIntegerField(
        "Routes communales (kms)", null=True, blank=True
    )
    departmental_roads = models.PositiveIntegerField(
        "Routes départementales (kms)", null=True, blank=True
    )
    tram_roads = models.PositiveIntegerField("Tramways (kms)", null=True, blank=True)
    lamppost_number = models.PositiveIntegerField(
        "Nombre de lampadaires", null=True, blank=True
    )

    library_number = models.PositiveIntegerField(
        "Nombre de bibliothèques", null=True, blank=True
    )
    medialibrary_number = models.PositiveIntegerField(
        "Nombre de mediathèques", null=True, blank=True
    )
    theater_number = models.PositiveIntegerField(
        "Nombre de théâtres", null=True, blank=True
    )
    museum_number = models.PositiveIntegerField(
        "Nombre de musées", null=True, blank=True
    )

    kindergarten_number = models.PositiveIntegerField(
        "Nombre d'écoles maternelles", null=True, blank=True
    )
    primary_school_number = models.PositiveIntegerField(
        "Nombre d'écoles primaires", null=True, blank=True
    )
    middle_school_number = models.PositiveIntegerField(
        "Nombre de collèges", null=True, blank=True
    )
    high_school_number = models.PositiveIntegerField(
        "Nombre de lycées", null=True, blank=True
    )
    university_number = models.PositiveIntegerField(
        "Nombre d'universités", null=True, blank=True
    )

    gymnasium_number = models.PositiveIntegerField(
        "Nombre de gymnases et salles de sport", null=True, blank=True
    )
    sports_ground_number = models.PositiveIntegerField(
        "Nombre de stades et structures extérieures", null=True, blank=True
    )
    swimming_pool_number = models.PositiveIntegerField(
        "Nombre de piscines", null=True, blank=True
    )

    place_of_worship_number = models.PositiveIntegerField(
        "Nombre de lieux de cultes", null=True, blank=True
    )
    cemetery_number = models.PositiveIntegerField(
        "Nombre de cimetières", null=True, blank=True
    )

    beneficiaries = models.ManyToManyField(
        "accounts.User", verbose_name="Bénéficiaires", blank=True
    )

    favorite_projects = models.ManyToManyField(
        "projects.Project",
        verbose_name="Projets favoris",
        related_name="organization_favorite",
        blank=True,
    )

    perimeter = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="Périmètre de la structure",
        on_delete=models.PROTECT,
        help_text="Sur quel périmètre la structure intervient-elle ?",
        null=True,
        blank=True,
    )
    perimeter_region = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="Région de la structure",
        on_delete=models.PROTECT,
        help_text="Sur quelle région la structure intervient-elle ?",
        null=True,
        blank=True,
        related_name="organization_region",
    )
    perimeter_department = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="Département de la structure",
        on_delete=models.PROTECT,
        help_text="Sur quel département la structure intervient-elle ?",
        null=True,
        blank=True,
        related_name="organization_department",
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Structure"
        verbose_name_plural = "Structures"

    def details_completed(self):
        return self.zip_code and self.city_name and self.perimeter is not None

    def __str__(self):
        return self.name

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def set_perimeters(self):
        """Set the object's region and department perimeters if it is missing."""
        if self.perimeter and self.perimeter.scale in [
            Perimeter.SCALES.commune,
            Perimeter.SCALES.epci,
            Perimeter.SCALES.department,
            Perimeter.SCALES.region,
        ]:
            # We might have EPCI across two regions.
            regions = get_all_related_perimeters(
                self.perimeter.id, direction="up", scale=Perimeter.SCALES.region
            )
            # In that case, we arbitrarily take the first one.
            # Knowing the commune of the EPCI's siège would help.
            region = regions.first()

            # We might have EPCI across two/three departments.
            departments = get_all_related_perimeters(
                self.perimeter.id, direction="up", scale=Perimeter.SCALES.department
            )
            # In that case, we arbitrarily take the first one.
            # Knowing the commune of the EPCI's siège would help.
            department = departments.first()

            self.perimeter_region = region
            self.perimeter_department = department

    def save(self, *args, **kwargs):
        self.set_slug()
        self.set_perimeters()
        return super().save(*args, **kwargs)
