from os.path import splitext

from django.db import models
from django.db.models import Q
from django.db.models.expressions import RawSQL
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

from aids.models import AidWorkflow


def logo_upload_to(instance, filename) -> str:
    """Rename uploaded files with the object's slug."""

    _, extension = splitext(filename)
    return f"backers/{instance.slug}_logo{extension}"


class BackerCategory(models.Model):
    """Represents a category of backers."""

    name = models.CharField("Nom", max_length=256, db_index=True)
    slug = models.SlugField(
        "Fragment d’URL", help_text="Laissez vide pour autoremplir", blank=True
    )
    order = models.PositiveIntegerField("Rang", blank=False, default=1)

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Catégorie de porteurs"
        verbose_name_plural = "Catégories de porteurs"
        ordering = ["order"]

    def __str__(self):
        return self.name

    @property
    def id_slug(self):
        return "{}-{}".format(self.id, self.slug)

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)


class BackerSubCategory(models.Model):
    """Represents a subcategory of backers."""

    name = models.CharField("Nom", max_length=256, db_index=True)
    slug = models.SlugField(
        "Fragment d'url", help_text="Laissez vide pour autoremplir", blank=True
    )
    category = models.ForeignKey(
        "BackerCategory",
        verbose_name="Catégorie de porteurs",
        related_name="backer_subcategories",
        on_delete=models.PROTECT,
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Sous-Catégorie de porteurs"
        verbose_name_plural = "Sous-Catégories de porteurs"

    def __str__(self):
        return self.name

    @property
    def id_slug(self):
        return "{}-{}".format(self.id, self.slug)

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)


class BackerGroup(models.Model):
    """Represents a group of backers."""

    name = models.CharField("Nom", max_length=256, db_index=True)
    slug = models.SlugField(
        "Fragment d’URL", help_text="Laissez vide pour autoremplir", blank=True
    )
    subcategory = models.ForeignKey(
        "BackerSubCategory",
        verbose_name="Sous-Catégorie de porteurs",
        related_name="backer_group",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Groupe de porteurs"
        verbose_name_plural = "Groupes de porteurs"

    def __str__(self):
        return self.name

    @property
    def id_slug(self):
        return "{}-{}".format(self.id, self.slug)

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)


class BackerQuerySet(models.QuerySet):
    """Custom queryset with additional filtering methods for backers."""

    def has_financed_aids(self):
        """Only return backers with financed_aids."""

        return self.exclude(financed_aids=None)

    def has_published_financed_aids(self):
        """Only return backers with published financed_aids."""

        qs = self.filter(financed_aids__status=AidWorkflow.states.published).distinct()
        return qs

    def has_logo(self):
        """Only return backers with a logo."""

        return self.exclude(Q(logo="") | Q(logo=None))

    def can_be_displayed_on_homepage(self):
        """Only return spotlighted backers with a logo."""

        return self.filter(is_spotlighted=True).has_logo()

    def annotate_aids_count(self, related_fields, annotation_name):
        """Annotate the queryset with the number of related aids.

        We have to use a custom raw sql method because it's impossible to
        `annotate` the same query several times.

        See this bug:
        https://code.djangoproject.com/ticket/10060#comment:67
        """
        raw_sql = """
            SELECT COUNT(*)
            FROM {model} as model
            WHERE model.backer_id = backers_backer.id
        """.format(
            model=related_fields.through._meta.db_table
        )
        annotation = {annotation_name: RawSQL(raw_sql, [])}
        return self.annotate(**annotation)


class Backer(models.Model):
    """Represents an entity that backs aids."""

    objects = BackerQuerySet.as_manager()

    name = models.CharField("Nom", max_length=256, db_index=True)
    slug = models.SlugField(
        "Fragment d’URL", help_text="Laissez vide pour autoremplir", blank=True
    )
    description = models.TextField(
        "Description complète du porteur d’aides", default="", blank=True
    )

    logo = models.FileField(
        "Logo du porteur",
        null=True,
        blank=True,
        upload_to=logo_upload_to,
        help_text="Évitez les fichiers trop lourds. Préférez les fichiers SVG.",
    )
    external_link = models.URLField(
        "Lien externe",
        null=True,
        blank=True,
        help_text="L’URL externe vers laquelle renvoie un clic sur le logo du porteur",
    )

    perimeter = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="Périmètre",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    is_corporate = models.BooleanField("Porteur d’aides privé ?", default=False)
    is_spotlighted = models.BooleanField(
        "Le porteur est-il mis en avant ?",
        default=False,
        help_text="Si le porteur est mis en avant, son logo apparaît sur la page d’accueil",
    )

    group = models.ForeignKey(
        "BackerGroup",
        verbose_name="Groupe de porteurs",
        related_name="backers",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # SEO
    meta_title = models.CharField(
        "Titre (balise meta)",
        max_length=180,
        blank=True,
        default="",
        help_text="""Le titre qui sera affiché dans les SERPs.
        Il est recommandé de le garder < 60 caractères.
        Laissez vide pour réutiliser le nom du porteur d’aides.""",
    )
    meta_description = models.TextField(
        "Description (balise meta)",
        blank=True,
        default="",
        max_length=256,
        help_text="Sera affichée dans les SERPs. À garder < 120 caractères.",
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Porteur"
        verbose_name_plural = "Porteurs"

    def __str__(self):
        return self.name

    @property
    def id_slug(self):
        return "{}-{}".format(self.id, self.slug)

    def get_absolute_url(self):
        url_args = [self.id]
        if self.slug:
            url_args.append(self.slug)
        return reverse("backer_detail_view", args=url_args)

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)

    def has_logo(self):
        return bool(self.logo.name)
