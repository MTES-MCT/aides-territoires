from django.db import models
from django.db.models import Value
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.indexes import GinIndex


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

    keywords_list = models.CharField(
        "liste de mots clés", max_length=1800, null=True, blank=True
    )

    # This field is used to index searchable text content
    search_vector_keywords_list = SearchVectorField(
        "liste de mots clés sans accents (Pour indexation)", null=True
    )

    class Meta:
        verbose_name = "Liste de synonymes"
        verbose_name_plural = "Listes de synonymes"
        ordering = ["name"]
        indexes = [
            GinIndex(fields=["search_vector_keywords_list"]),
        ]

    def __str__(self):
        return self.name

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def set_search_vector_keywords_list(self):
        """Update the full text unaccented cache field."""

        search_vector_keywords_list = SearchVector(
            Value(self.keywords_list, output_field=models.CharField()),
            weight="A",
            config="french_unaccent",
        )

        self.search_vector_keywords_list = search_vector_keywords_list

    def sort_keywords_list(self):
        """Sort keywords_list by alpha."""
        harmonized_keywords_list = self.keywords_list.replace(', ', ',')
        sorted_keywords_list = sorted(harmonized_keywords_list.split(","))
        self.keywords_list = ", ".join(sorted_keywords_list)

    @property
    def id_slug(self):
        """Set the object's id_slug for autocomplete purpose."""
        return f"{self.id}-synonyms-{self.name}"

    @property
    def autocomplete_name(self):
        return f"Champ lexical du mot «{self.name}»"

    def save(self, *args, **kwargs):
        self.set_slug()
        self.sort_keywords_list()
        self.set_search_vector_keywords_list()
        return super().save(*args, **kwargs)
