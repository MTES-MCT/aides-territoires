from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Keyword(models.Model):

    name = models.CharField("Nom", max_length=70)
    slug = models.SlugField("Fragment d'url")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Mot clé"
        verbose_name_plural = "Mots clé"
        ordering = ["-date_created"]

    def __str__(self):
        return self.name

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)


class SynonymList(models.Model):

    name = models.CharField("Nom de la liste", max_length=70)
    slug = models.SlugField("Fragment d'url")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    keywords = models.ManyToManyField(
        "keywords.Keyword",
        verbose_name="Mots clé",
        related_name="synonymList",
        blank=True,
    )

    class Meta:
        verbose_name = "Liste de synonymes"
        verbose_name_plural = "Listes de synonymes"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    @property
    def keywords_str(self):

        keywords_name_list = []
        for keyword in self.keywords.all():
            keywords_name_list.append(keyword.name)
        keywords_name_str = ", ".join(keywords_name_list)
        return keywords_name_str

    @property
    def autocomplete_name(self):
        return f"Champ lexical du mot «{self.name}»"

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)
