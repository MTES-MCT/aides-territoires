from os.path import splitext

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def logo_upload_to(instance, filename):
    """Rename uploaded files with the object's slug."""
    _, extension = splitext(filename)
    name = instance.slug
    filename = "programs/{}_logo{}".format(name, extension)
    return filename


class Program(models.Model):
    """Represents a single aid program.

    Real-life examples of such programs:
      - Territoires d'Industrie
      - Action Cœur de Ville

    Aid programs regroup new or existing aids, and generally
    are limited to a specific perimeter.
    """

    name = models.CharField(_("Name"), max_length=256)
    slug = models.SlugField(_("Slug"))
    short_description = models.CharField(
        _("Short description"),
        help_text=_("Will only appear in search results. 300 chars. max."),
        max_length=300,
    )
    description = models.TextField(_("Description"))

    logo = models.FileField(
        _("Logo"),
        null=True,
        blank=True,
        upload_to=logo_upload_to,
        help_text=_("Make sure the file is not too heavy. Prefer svg files."),
    )

    perimeter = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="Périmètre",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # SEO
    meta_title = models.CharField(
        _("Meta title"),
        max_length=60,
        blank=True,
        default="",
        help_text=_(
            "This will be displayed in SERPs. "
            "Keep it under 60 characters. "
            "Leave empty and we will reuse the program's name."
        ),
    )
    meta_description = models.TextField(
        _("Meta description"),
        blank=True,
        default="",
        max_length=120,
        help_text=_(
            "This will be displayed in SERPs. " "Keep it under 120 characters."
        ),
    )

    date_created = models.DateTimeField(_("Date created"), default=timezone.now)

    class Meta:
        verbose_name = _("Aid program")
        verbose_name_plural = _("Aid programs")

    def __str__(self):
        return self.name

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)
