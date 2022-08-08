from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex

from model_utils import Choices

from core.utils import remove_accents


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

    scale = models.PositiveIntegerField(_("Scale"), choices=SCALES)
    name = models.CharField(_("Name"), max_length=128)
    code = models.CharField(
        _("Code"),
        max_length=16,
        help_text=_("Internal usage only, not relevant for Ad-hoc perimeters"),
    )

    contained_in = models.ManyToManyField(
        "geofr.Perimeter",
        verbose_name=_("Contained in"),
        related_name="contains",
        blank=True,
    )
    manually_created = models.BooleanField(_("Manually created"), default=False)
    is_visible_to_users = models.BooleanField(
        _("The perimeter is visible to users"), default=True
    )
    date_obsolete = models.DateTimeField(
        "date d'obsolescence",
        help_text="Date de mise à jour des périmètres à laquelle \
            ce périmètre ne figurait plus dans les sources officielles",
        blank=True,
        null=True,
    )
    is_obsolete = models.BooleanField("Ce périmètre n'existe plus", default=False)

    continent = models.CharField(_("Continent"), max_length=2, default="EU")
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
    epci = models.CharField(_("EPCI"), max_length=32, blank=True)  # INSEE COG
    basin = models.CharField(
        _("Drainage basin"), max_length=32, blank=True  # Sandre code
    )
    zipcodes = ArrayField(
        verbose_name=_("Zip codes"),
        base_field=models.CharField(max_length=8),
        null=True,
        blank=True,
    )
    is_overseas = models.BooleanField(verbose_name=_("Is overseas?"), null=True)

    # Counters: used only at Department level
    # script-updated nightly
    backers_count = models.PositiveSmallIntegerField(
        verbose_name="nombre de porteurs", null=True, blank=True
    )
    programs_count = models.PositiveSmallIntegerField(
        verbose_name="nombre de programmes", null=True, blank=True
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
        _("Name without accent (for indexing purpose)"), max_length=128
    )

    date_created = models.DateTimeField(_("Date created"), default=timezone.now)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True)

    class Meta:
        verbose_name = _("Perimeter")
        verbose_name_plural = _("Perimeters")
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
        help_text="Liste d'identifiants INSEE de communes",
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
