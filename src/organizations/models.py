from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from core.fields import ChoiceArrayField
from model_utils import Choices
from geofr.models import Perimeter
from geofr.services.validators import validate_siren, validate_siret
from geofr.utils import get_all_related_perimeters
from organizations.constants import (
    INTERCOMMUNALITY_TYPES,
    ORGANIZATION_TYPES_COLLECTIVITIES_SINGULAR,
    ORGANIZATION_TYPES_SINGULAR_ALL_CHOICES,
    POPULATION_STRATAS,
)


class OrganizationQuerySet(models.QuerySet):
    def communes(self, values=None):
        """
        Returns a list of the communal organizations
        """
        communes = self.filter(perimeter__scale=Perimeter.SCALES.commune)
        if values:
            communes = communes.values(*values)

        return communes.order_by("perimeter__insee")

    def obsolete_perimeters(self, values=None):
        """
        Returns a list of the organizations linked to an obsolete perimeter
        """
        orgs = self.filter(perimeter__is_obsolete=True)
        if values:
            orgs = orgs.values(*values)

        return orgs


class Organization(models.Model):
    ORGANIZATION_TYPE_CHOICES = ORGANIZATION_TYPES_SINGULAR_ALL_CHOICES
    INTERCOMMUNALITY_TYPES_CHOICES = Choices(*INTERCOMMUNALITY_TYPES)

    objects = OrganizationQuerySet.as_manager()

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

    insee_code = models.CharField(
        "code Insee",
        max_length=5,
        help_text="Identifiant officiel défini dans le Code officiel géographique",
        blank=True,
        null=True,
    )

    siren_code = models.CharField(
        "numéro Siren",
        max_length=9,
        help_text="Identifiant officiel à 9 chiffres défini dans la base SIREN",
        validators=[validate_siren],
        blank=True,
        null=True,
    )

    siret_code = models.CharField(
        "numéro Siret",
        max_length=14,
        help_text="Identifiant officiel à 14 chiffres défini dans la base SIREN",
        validators=[validate_siret],
        blank=True,
        null=True,
    )
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
        "Nombre de pistes d’athlétisme", null=True, blank=True
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
        verbose_name="Porteur d’aides",
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
        """
        if self.perimeter and self.perimeter.scale == Perimeter.SCALES.commune:
            if not self.inhabitants_number:
                self.inhabitants_number = self.perimeter.population

    def set_population_strata(self):
        """
        Set the population strata value for municipalities.

        Note: A match-case implementation would lower the cognitive complexity
        but is not really actually more readable and has worse performance.
        """
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

        collectivity_types = [x[0] for x in ORGANIZATION_TYPES_COLLECTIVITIES_SINGULAR]

        if (
            self.organization_type
            and self.organization_type[0] in collectivity_types
            and self.perimeter
            and self.perimeter.scale in collectivity_scales
        ):
            # Codes fields
            insee_code = self.perimeter.insee
            if insee_code and not self.insee_code:
                self.insee_code = insee_code

            siren_code = self.perimeter.siren
            if siren_code and not self.siren_code:
                self.siren_code = siren_code

            siret_code = self.perimeter.siret
            if siret_code and not self.siret_code:
                self.siret_code = siret_code

            ape_code = self.perimeter.get_perimeter_data_by_property("ape_code")
            if ape_code and not self.ape_code:
                # We store the APE code without the standard dot for some reason
                self.ape_code = ape_code.replace(".", "")

            # Address fields
            address_street = self.perimeter.get_perimeter_data_by_property(
                "address_street"
            )
            if address_street and not self.address:
                self.address = address_street

            city_name = self.perimeter.get_perimeter_data_by_property(
                "address_city_name"
            )
            if city_name and not self.city_name:
                self.city_name = city_name

            zip_code = self.perimeter.get_perimeter_data_by_property("address_zipcode")
            if zip_code and not self.zip_code:
                self.zip_code = zip_code

            intercommunality_type = self.perimeter.get_perimeter_data_by_property(
                "type_epci"
            )
            if intercommunality_type and not self.intercommunality_type:
                self.intercommunality_type = intercommunality_type

    def save(self, *args, **kwargs):
        self.set_slug()
        self.set_perimeters()
        self.set_population()
        self.set_population_strata()
        self.set_extra_data()
        return super().save(*args, **kwargs)
