from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class Project(models.Model):

    name = models.CharField(
        "Nom du projet", max_length=256, null=False, blank=False, db_index=True
    )
    slug = models.SlugField(
        "Fragment d’URL", help_text="Laisser vide pour autoremplir.", blank=True
    )
    description = models.TextField(
        "Description complète du projet", default="", blank=True
    )
    key_words = models.TextField(
        "Mots-clés",
        help_text="mots-clés associés au projet",
        default="",
        blank=True,
    )
    organizations = models.ManyToManyField(
        "organizations.Organization", verbose_name="Structures", blank=True
    )
    author = models.ManyToManyField("accounts.User", verbose_name="Auteur", blank=True)

    is_published = models.BooleanField("Publié?", default=False)

    project_types = models.ManyToManyField(
        "keywords.SynonymList", verbose_name="Types de projet", blank=True
    )

    due_date = models.DateField("Date d’échéance", null=True, blank=True)

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "projet"
        verbose_name_plural = "projets"
        ordering = ["-id"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        url_args = [self.id]
        if self.slug:
            url_args.append(self.slug)
        return reverse("project_detail_view", args=url_args)

    @property
    def id_slug(self):
        return "{}-{}".format(self.id, self.slug)

    @property
    def organization(self):
        return self.organizations.first()

    def set_slug(self):
        """Set the object's slug"""
        if not self.id:
            full_title = "{}-{}".format(str(uuid4())[:4], self.name)
            self.slug = slugify(full_title)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)
