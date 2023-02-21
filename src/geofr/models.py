from django.db import models
from django.db.models import F
from django.db.models.query import QuerySet
from django.db.models.functions import ACos, Cos, Radians, Sin, Least
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex

from model_utils import Choices

from core.utils import remove_accents


class PerimeterQuerySet(models.QuerySet):
    def departments(self, values=None):
        """
        Returns a list of the departments
        - with a slug
        - sorted by code
        - and so that the Corsican ones are listed between 19 and 21
        """
        departments = self.filter(scale=Perimeter.SCALES.department, is_obsolete=False)
        if values:
            departments = departments.values(*values)
        departments = departments.order_by("code")
        departments_list = []

        # perimeters currently don't have a proper slug
        for department in departments:
            if values:
                department["slug"] = slugify(department["name"])
            else:
                department.slug = slugify(department.name)

            departments_list.append(department)

        def department_code_key(department):
            """Sort the departments so that Corsican ones are between 19 and 21."""
            if values:
                code = department["code"]
            else:
                code = department.code
            if code == "2A":
                return "20"
            elif code == "2B":
                return "20.5"
            else:
                return code

        departments_list = sorted(departments_list, key=department_code_key)

        return departments_list

    def communes_by_distance(
        self, latitude: float, longitude: float, radius: int | None = None
    ) -> QuerySet:
        """
        Returns a queryset of the communes closest to the given coordinates,
        with a calculation based on the Haversine formula.

        The queryset can be constricted to communes within a given radus.

        The operations are made on floats, which can cause rounding errors,
        so we use "Least" to ensure we don't try to calculate the
        arccosine of a value > 1.0, which would result in a math error.
        """

        # Filtering out obsolete communes because they don't have coordinates
        qs = self.filter(scale=Perimeter.SCALES.commune, is_obsolete=False)
        qs = qs.annotate(
            distance=ACos(
                Least(
                    Cos(Radians(latitude))
                    * Cos(Radians(F("latitude")))
                    * Cos(Radians(F("longitude")) - Radians(longitude))
                    + Sin(Radians(latitude)) * Sin(Radians(F("latitude"))),
                    1.0,
                )
            )
            * 6371
        )

        if radius:
            qs = qs.filter(distance__lte=radius)

        return qs.order_by("distance")


class Perimeter(models.Model):
    """
    Represents a single application perimeter for an Aid.

    Each perimeter represents a location (e.g a region, a department, a
    commune…) and contains data about where it is located.

    E.g: the commune of Montpellier is located in Hérault, Occitanie, France, Europe.

    Since nothing is simple when administration is involved, some perimeters
    e.g epcis can be spread over several departments / regions.

    Drainage basins are another edge case, since they are independant from any
    existing legal borders.
    https://fr.wikipedia.org/wiki/Bassin_hydrographique
    """

    objects = PerimeterQuerySet.as_manager()

    SCALES_TUPLE = (
        (1, "commune", "Commune"),
        (5, "epci", "EPCI"),
        (8, "basin", "Bassin hydrographique"),
        (10, "department", "Département"),
        (15, "region", "Région"),
        (16, "overseas", "Outre-mer"),
        (17, "mainland", "Métropole"),
        (18, "adhoc", "Ad-hoc"),
        (20, "country", "Pays"),
        (25, "continent", "Continent"),
    )
    SCALES = Choices(*SCALES_TUPLE)

    scale = models.PositiveIntegerField("Échelle", choices=SCALES)
    name = models.CharField("Nom", max_length=128)
    code = models.CharField(
        "Code",
        max_length=16,
        help_text="Usage interne uniquement, non pertinent pour les périmètres Ad-hoc.",
    )

    contained_in = models.ManyToManyField(
        "geofr.Perimeter",
        verbose_name="Contenu dans",
        related_name="contains",
        blank=True,
    )
    manually_created = models.BooleanField("Création manuelle", default=False)
    is_visible_to_users = models.BooleanField(
        "Le périmètre est visible pour les utilisateurs", default=True
    )
    date_obsolete = models.DateTimeField(
        "date d’obsolescence",
        help_text="Date de mise à jour des périmètres à laquelle \
            ce périmètre ne figurait plus dans les sources officielles",
        blank=True,
        null=True,
    )
    is_obsolete = models.BooleanField("Ce périmètre n’existe plus", default=False)

    continent = models.CharField("Continent", max_length=2, default="EU")
    country = models.CharField("Pays", max_length=3, default="FRA")  # ISO_3166-3 codes
    regions = ArrayField(  # Array of region codes (INSEE COG)
        verbose_name="Régions",
        base_field=models.CharField(max_length=2),
        default=list,
        blank=True,
    )
    departments = ArrayField(  # Array of depts codes (INSEE COG)
        verbose_name="Départements",
        base_field=models.CharField(max_length=3),
        default=list,
        blank=True,
    )
    epci = models.CharField("EPCI", max_length=32, blank=True)  # INSEE COG
    basin = models.CharField(
        "Bassin hydrographique", max_length=32, blank=True, help_text="Code Sandre"
    )
    zipcodes = ArrayField(
        verbose_name="Codes postaux",
        base_field=models.CharField(max_length=8),
        null=True,
        blank=True,
    )
    is_overseas = models.BooleanField(verbose_name="En Outre-mer ?", null=True)

    population = models.PositiveIntegerField(
        verbose_name="population", null=True, blank=True
    )  # Sourced from Banatic

    # Location, stored as floats to avoid using GeoDjango
    # and its many dependencies
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    # Sourced from API Découpage Administratif - (API Geo)

    # Counters: used only at Department level
    # script-updated nightly
    backers_count = models.PositiveSmallIntegerField(
        verbose_name="nombre de porteurs", null=True, blank=True
    )
    programs_count = models.PositiveSmallIntegerField(
        verbose_name="nombre de programmes", null=True, blank=True
    )
    projects_count = models.PositiveSmallIntegerField(
        verbose_name="nombre de projets subventionnés", null=True, blank=True
    )
    live_aids_count = models.PositiveSmallIntegerField(
        verbose_name="nombre d’aides live", null=True, blank=True
    )

    categories_count = models.PositiveSmallIntegerField(
        verbose_name="nombre de catégories", null=True, blank=True
    )

    # This field is used to store the name without accent, for indexing.
    # We recently updated the perimeter search to ignore accents, and at first
    # we were using postgres' unaccent extension.
    # We ran into an issue where the trigram index was not being used anymore
    # bumping the querytime from a few ms to more than 300ms.
    # Since it's kinda hard to add an index on an unaccent expression, it's
    # just easier to store an index the unaccented version of the name.
    unaccented_name = models.CharField(
        "Nom sans accents (pour l’indexation)", max_length=128
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "périmètre"
        unique_together = (("scale", "code"),)
        indexes = [
            GinIndex(name="name_trgm", fields=["name"], opclasses=["gin_trgm_ops"]),
            GinIndex(
                name="unaccented_name_trgm",
                fields=["unaccented_name"],
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        if not self.scale:
            return ""

        if self.scale == self.SCALES.commune and self.zipcodes:
            _str = "{} ({} – {})".format(
                self.name, self.get_scale_display(), ", ".join(self.zipcodes)
            )
        elif self.scale <= self.SCALES.region:
            _str = "{} ({})".format(self.name, self.get_scale_display())
        else:
            _str = self.name

        return _str

    @property
    def id_slug(self):
        return "{}-{}".format(self.id, slugify(self.name))

    def save(self, *args, **kwargs):
        self.unaccented_name = remove_accents(self.name)
        return super().save(*args, **kwargs)

    def get_communes_within_radius(self, radius: int) -> QuerySet:
        """
        Returns a list of the closest communes objects sorted by distance
        within a radius (in kilometers) from a center commune object.
        """
        if self.scale != Perimeter.SCALES.commune:
            raise ValueError("The center object must be a commune itself")
        return Perimeter.objects.communes_by_distance(
            latitude=self.latitude, longitude=self.longitude, radius=radius
        )


class PerimeterImport(models.Model):
    """
    Represents the necessary data to run an Import task for a big perimeter.
    """

    adhoc_perimeter = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="périmètre adhoc",
        on_delete=models.CASCADE,
        help_text="Périmètre à définir",
    )
    city_codes = ArrayField(
        models.CharField(max_length=5),
        verbose_name="périmètres contenus",
        help_text="Liste d’identifiants INSEE de communes",
    )
    author = models.ForeignKey(
        "accounts.User",
        verbose_name="Auteur",
        on_delete=models.PROTECT,
        help_text="Créateur du périmètre",
    )
    is_imported = models.BooleanField("import effectué ?", default=False)
    date_imported = models.DateTimeField("date d’import", null=True, blank=True)

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "import périmètre"
        verbose_name_plural = "imports périmètre"

    def __str__(self):
        return f"{self.id} - {self.adhoc_perimeter.name}"


class PerimeterData(models.Model):
    """
    Allows to import extra data for perimeters, without adding extra fields to the main model for
    things that concern only a subset of EPCIs (only communes for now)
    This allows for a triplet-style storing of data, with
    perimeter - property - value

    The list of currently used properties is available through the get_properties() method
    """

    perimeter = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="périmètre",
        on_delete=models.CASCADE,
        help_text="Périmètre pour lequel les données sont importées",
    )

    # should be property but this is a reserved keyword in Python
    prop = models.CharField(verbose_name="propriété", max_length=100)
    value = models.CharField(verbose_name="valeur", max_length=255)

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    def __str__(self):
        return f"{self.perimeter} – {self.prop}: {self.value}"

    @classmethod
    def get_properties(cls) -> QuerySet:
        return PerimeterData.objects.values_list("prop", flat=True).distinct()

    class Meta:
        verbose_name = "donnée de périmètre"
        verbose_name_plural = "données de périmètre"
        unique_together = (("perimeter", "prop"),)
