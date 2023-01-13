from os.path import splitext

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from pages.models import Tab


def logo_upload_to(instance, filename):
    """Rename uploaded files with the object's slug."""
    _, extension = splitext(filename)
    filename = f"programs/{instance.slug}_logo{extension}"
    return filename


class ProgramQuerySet(models.QuerySet):
    """Custom queryset with additional filtering methods for programs."""

    def has_aids(self):
        """Only return programs with aids."""

        return self.exclude(aids=None)

    def has_logo(self):
        """Only return programs with a logo."""

        return self.exclude(models.Q(logo="") | models.Q(logo=None))

    def can_be_displayed_on_homepage(self):
        """Only return spotlighted programs with a logo."""

        return self.filter(is_spotlighted=True).has_logo()


class Program(models.Model):
    """Represents a single aid program.

    Real-life examples of such programs:
      - Territoires d’Industrie
      - Action Cœur de Ville

    Aid programs regroup new or existing aids, and generally
    are limited to a specific perimeter.
    """

    objects = ProgramQuerySet.as_manager()

    name = models.CharField("Nom", max_length=256)
    slug = models.SlugField("Fragment d’URL")
    short_description = models.CharField(
        "Brève description",
        help_text="300 caractères max. Résultats de recherche uniquement.",
        max_length=300,
    )
    description = models.TextField("Description")

    logo = models.FileField(
        "Logo",
        null=True,
        blank=True,
        upload_to=logo_upload_to,
        help_text="Évitez les fichiers trop lourds. Préférez les fichiers SVG.",
    )

    perimeter = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="Périmètre",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    is_spotlighted = models.BooleanField(
        "Le programme est-il mis en avant ?",
        default=False,
        help_text="Si le programme est mis en avant, son logo apparaît sur la page d’accueil",
    )

    # SEO
    meta_title = models.CharField(
        "Titre (balise meta)",
        max_length=60,
        blank=True,
        default="",
        help_text="""
        Le titre qui sera affiché dans les SERPs. Il est recommandé de le garder < 60
        caractères. Laissez vide pour réutiliser le nom du programme.
        """,
    )
    meta_description = models.TextField(
        "Description (balise meta)",
        blank=True,
        default="",
        max_length=120,
        help_text="Sera affichée dans les SERPs. À garder < 120 caractères.",
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Programme d’aides"
        verbose_name_plural = "Programmes d’aides"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        url_args = [self.slug]
        return reverse("program_detail", args=url_args)


class ProgramTab(Tab):
    """
    Proxy class to make Tab model available for programs
    as a Tab.
    """

    class Meta:
        proxy = True
        verbose_name = "onglet programme"
        verbose_name_plural = "onglets programme"
