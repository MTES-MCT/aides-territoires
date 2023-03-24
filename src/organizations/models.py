from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from core.fields import ChoiceArrayField
from model_utils import Choices
from geofr.models import Perimeter
from geofr.utils import get_all_related_perimeters
from organizations.constants import (
    INTERCOMMUNALITY_TYPES,
    ORGANIZATION_TYPES_SINGULAR_ALL_CHOICES,
    POPULATION_STRATAS,
)


class Organization(models.Model):
    ORGANIZATION_TYPE_CHOICES = ORGANIZATION_TYPES_SINGULAR_ALL_CHOICES
    INTERCOMMUNALITY_TYPES_CHOICES = Choices(*INTERCOMMUNALITY_TYPES)

    name = models.CharField("Nom", max_length=256, db_index=True)
    slug = models.SlugField(
        "Fragment d’URL", help_text="Laisser vide pour autoremplir.", blank=True
    )
    organization_type = ChoiceArrayField(
        verbose_name="Type de structure",
        null=True,
        blank=True,
        base_field=models.CharField(max_length=32, choices=ORGANIZATION_TYPE_CHOICES),
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
        "Nombre d’habitants", null=True, blank=True
    )
    voters_number = models.PositiveIntegerField(
        "Nombre de votants", null=True, blank=True
    )
    corporates_number = models.PositiveIntegerField(
        "Nombre d’entreprises", null=True, blank=True
    )
    shops_number = models.PositiveIntegerField(
        "Nombre de commerces", null=True, blank=True
    )
    associations_number = models.PositiveIntegerField(
        "Nombre d’associations", null=True, blank=True
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
    bridge_number = models.PositiveIntegerField(
        "Nombre de ponts", null=True, blank=True
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
    cinema_number = models.PositiveIntegerField(
        "Nombre de cinéma", null=True, blank=True
    )
    museum_number = models.PositiveIntegerField(
        "Nombre de musées", null=True, blank=True
    )
    nursery_number = models.PositiveIntegerField(
        "Nombre de crèches", null=True, blank=True
    )
    kindergarten_number = models.PositiveIntegerField(
        "Nombre d’écoles maternelles", null=True, blank=True
    )
    primary_school_number = models.PositiveIntegerField(
        "Nombre d’écoles primaires", null=True, blank=True
    )
    rec_center_number = models.PositiveIntegerField(
        "Nombre de centres de loisirs", null=True, blank=True
    )
    middle_school_number = models.PositiveIntegerField(
        "Nombre de collèges", null=True, blank=True
    )
    high_school_number = models.PositiveIntegerField(
        "Nombre de lycées", null=True, blank=True
    )
    university_number = models.PositiveIntegerField(
        "Nombre d’universités", null=True, blank=True
    )
    tennis_court_number = models.PositiveIntegerField(
        "Nombre de court de tennis", null=True, blank=True
    )
    football_field_number = models.PositiveIntegerField(
        "Nombre de terrains de football", null=True, blank=True
    )
    running_track_number = models.PositiveIntegerField(
        "Nombre de pistes d'athlétisme", null=True, blank=True
    )
    other_outside_structure_number = models.PositiveIntegerField(
        "Nombre de structures extérieures autres", null=True, blank=True
    )
    covered_sporting_complex_number = models.PositiveIntegerField(
        "Nombre de complexes sportifs couverts", null=True, blank=True
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
    protected_monument_number = models.PositiveIntegerField(
        "Nombre de monuments classés", null=True, blank=True
    )
    forest_number = models.PositiveIntegerField(
        "Nombre de forêts", null=True, blank=True
    )

    beneficiaries = models.ManyToManyField(
        "accounts.User", verbose_name="Bénéficiaires", blank=True
    )

    backer = models.ForeignKey(
        "backers.Backer",
        verbose_name="Porteur d'aides",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    favorite_projects = models.ManyToManyField(
        "projects.Project",
        verbose_name="Projets favoris",
        related_name="organization_favorite",
        blank=True,
    )

    is_imported = models.BooleanField(
        "Organisation importée ?",
        help_text="Cette organisation a-t-elle été importée ?",
        default=False,
    )
    imported_date = models.DateTimeField(
        "Date de l’import",
        help_text="Date à laquelle cette organisation a été importée",
        null=True,
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

    intercommunality_type = models.CharField(
        verbose_name="Type d’intercommunalité",
        max_length=5,
        choices=INTERCOMMUNALITY_TYPES_CHOICES,
        null=True,
        blank=True,
    )

    population_strata = models.CharField(
        verbose_name="Strate démographique",
        max_length=15,
        choices=POPULATION_STRATAS,
        null=True,
        blank=True,
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

    def set_population(self):
        """
        Set the population value for municipalities if it is missing
        Also set the strata value
        """
        if self.perimeter and self.perimeter.scale == Perimeter.SCALES.commune:
            if not self.inhabitants_number:
                self.inhabitants_number = self.perimeter.population

            if self.inhabitants_number is not None:
                if self.inhabitants_number < 500:
                    self.population_strata = "500-"
                elif self.inhabitants_number < 1000:
                    self.population_strata = "500_599"
                elif self.inhabitants_number < 2000:
                    self.population_strata = "1000_1999"
                elif self.inhabitants_number < 3500:
                    self.population_strata = "2000_3499"
                elif self.inhabitants_number < 5000:
                    self.population_strata = "3500_4999"
                elif self.inhabitants_number < 7500:
                    self.population_strata = "5000_7499"
                elif self.inhabitants_number < 10000:
                    self.population_strata = "7500_9999"
                elif self.inhabitants_number < 15000:
                    self.population_strata = "10000_14999"
                elif self.inhabitants_number < 20000:
                    self.population_strata = "15000_19999"
                elif self.inhabitants_number < 35000:
                    self.population_strata = "20000_34999"
                elif self.inhabitants_number < 50000:
                    self.population_strata = "35000_49999"
                elif self.inhabitants_number < 75000:
                    self.population_strata = "50000_74999"
                elif self.inhabitants_number < 100000:
                    self.population_strata = "75000_99999"
                elif self.inhabitants_number < 200000:
                    self.population_strata = "100000_199999"
                else:
                    self.population_strata = "200000+"

    def set_extra_data(self) -> None:
        """
        Set extra data gathered from the perimeter to
        the organization
        """
        collectivity_scales = (
            Perimeter.SCALES.commune,
            Perimeter.SCALES.epci,
            Perimeter.SCALES.department,
            Perimeter.SCALES.region,
        )

        if self.perimeter and self.perimeter.scale in collectivity_scales:
            siren = self.perimeter.siren
            if siren and not self.siren:
                self.siren = siren

    def save(self, *args, **kwargs):
        self.set_slug()
        self.set_perimeters()
        self.set_population()
        self.set_extra_data()
        return super().save(*args, **kwargs)
