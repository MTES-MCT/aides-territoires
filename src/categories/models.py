from django.db import models
from django.utils.translation import gettext_lazy as _


class Theme(models.Model):
    name = models.CharField(_("Name"), max_length=70)
    slug = models.SlugField(_("Slug"))
    short_description = models.TextField(_("Short description"), blank=True)

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=70)
    slug = models.SlugField(_("Slug"))
    short_description = models.TextField(
        _("Short description"), max_length=160, blank=True
    )
    theme = models.ForeignKey(
        "Theme",
        verbose_name=_("Theme"),
        related_name="categories",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name
