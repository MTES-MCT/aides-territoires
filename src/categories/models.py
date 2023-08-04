from django.db import models


class Theme(models.Model):
    """Thématique"""

    name = models.CharField("Nom", max_length=70)
    slug = models.SlugField("Fragment d’URL")
    short_description = models.TextField("Brève description", blank=True)

    class Meta:
        verbose_name = "Thématique"
        verbose_name_plural = "Thématiques"

    def __str__(self):
        return self.name


class Category(models.Model):
    """Sous-thématique"""

    name = models.CharField("Nom", max_length=70)
    slug = models.SlugField("Fragment d’URL")
    short_description = models.TextField(
        "Brève description", max_length=160, blank=True
    )
    theme = models.ForeignKey(
        "Theme",
        verbose_name="Thématique",
        related_name="categories",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "Sous-thématique"
        verbose_name_plural = "Sous-thématiques"

    def __str__(self):
        return self.name
