from os.path import splitext
from uuid import uuid4

from django.db import models
from django.db.models import Value, UniqueConstraint
from django.db.models.functions import Lower
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.indexes import GinIndex

from model_utils import Choices
from django_resized import ResizedImageField


def image_upload_to(instance, filename):
    """Rename uploaded files with the object's slug."""

    _, extension = splitext(filename)
    name = instance.slug
    filename = f"projects/{name}_image{extension}"
    return filename


class Project(models.Model):

    STATUS = Choices(
        ("draft", "Brouillon"),
        ("reviewable", "En revue"),
        ("published", "Publié"),
        ("deleted", "Supprimé"),
    )

    CONTRACT_LINK = Choices(
        ("CRTE", "CRTE"),
        ("PVD", "Petites Villes de Demain"),
        ("ACV1", "Action Coeur de Ville 1"),
        ("ACV2", "Action Coeur de Ville 2"),
        ("PCAET", "PCAET"),
    )

    PROJECT_STEPS = Choices(
        ("considered", "En réflexion"),
        ("ongoing", "En cours"),
        ("finished", "Réalisé"),
    )

    name = models.CharField(
        "Nom du projet", max_length=256, null=False, blank=False, db_index=True
    )
    slug = models.SlugField(
        "Fragment d’URL", help_text="Laisser vide pour autoremplir.", blank=True
    )
    description = models.TextField("Description du projet", default="", blank=True)
    private_description = models.TextField(
        "Notes internes du projet", default="", blank=True
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
    other_project_owner = models.CharField(
        "Autre maître d’ouvrage",
        max_length=180,
        null=True,
        blank=True,
    )
    author = models.ManyToManyField("accounts.User", verbose_name="Auteur", blank=True)

    is_public = models.BooleanField("Ce projet est-il public?", default=False)

    contract_link = models.CharField(
        "Appartenance à un plan/programme/contrat",
        max_length=10,
        choices=CONTRACT_LINK,
        blank=True,
        null=True,
    )

    project_types = models.ManyToManyField(
        "keywords.SynonymList",
        verbose_name="Types de projet",
        related_name="projects",
        blank=True,
    )

    project_types_suggestion = models.CharField(
        "Type de projet suggéré", max_length=256, blank=True
    )

    due_date = models.DateField("Date d’échéance", null=True, blank=True)

    step = models.CharField(
        "Avancement du projet",
        max_length=10,
        choices=PROJECT_STEPS,
        blank=True,
        null=True,
    )

    budget = models.PositiveIntegerField("Budget prévisionnel", null=True, blank=True)

    status = models.CharField(
        "Statut",
        max_length=10,
        choices=STATUS,
        default=STATUS.draft,
    )

    image = ResizedImageField(
        size=[714, 450],
        upload_to=image_upload_to,
        crop=["middle", "center"],
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"])],
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "projet"
        verbose_name_plural = "projets"
        ordering = ["-id"]

    def __str__(self):
        return self.name

    def is_published(self):
        return self.status == Project.STATUS.published

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


class ValidatedProject(models.Model):
    project_name = models.CharField(
        "Nom du projet",
        max_length=255,
        null=False,
        blank=False,
    )
    description = models.TextField(
        "Description du projet",
        default="",
        blank=True,
    )
    aid_name = models.CharField(
        "Nom de l’aide",
        max_length=180,
        null=False,
        blank=False,
    )
    project_linked = models.ForeignKey(
        "projects.Project",
        verbose_name="Projet lié",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    aid_linked = models.ForeignKey(
        "aids.Aid",
        verbose_name="Aide liée",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        verbose_name="Organisation porteuse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    financer_linked = models.ForeignKey(
        "backers.Backer",
        verbose_name="Porteur d’aides lié",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    financer_name = models.CharField(
        "Nom du porteur de l’aide obtenue",
        max_length=255,
        default="",
        blank=True,
    )
    budget = models.PositiveIntegerField("Budget définitif", null=True, blank=True)
    amount_obtained = models.PositiveIntegerField(
        "Montant obtenu", null=True, blank=True
    )
    date_obtained = models.DateTimeField(
        "Date de l’obtention",
        help_text="Date à laquelle l’aide a été obtenue par le porteur du projet",
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField("Date de création", default=timezone.now)

    search_vector_unaccented_validated_project = SearchVectorField(
        "Search vector unaccented_validated_project", null=True
    )

    # Manually setting a unique import_uniqueid because get_or_create fails at
    # detecting duplicates over so many fields.
    # See the import script for format.
    import_uniqueid = models.CharField(
        "Identifiant d’import unique",
        max_length=64,
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Projet subventionné"
        verbose_name_plural = "Projets subventionnés"
        ordering = ["project_name"]
        indexes = [
            GinIndex(fields=["search_vector_unaccented_validated_project"]),
        ]
        constraints = [
            UniqueConstraint(
                Lower("project_name"),
                Lower("aid_name"),
                "financer_name",
                "amount_obtained",
                "date_obtained",
                name="unique_projectname_aidname_financername_amount_date",
            ),
        ]

    def __str__(self):
        return self.project_name

    def set_search_vector_unaccented_validated_project(self):
        """Update the full text unaccented cache field."""

        # Note: we use `SearchVector(Value(self.field))` instead of
        # `SearchVector('field')` because the latter only works for updates,
        # not when inserting new records.
        #
        # Note 2: we have to pass the financers parameter instead of using
        # `self.financers.all()` because that last expression would not work
        # during an object creation.
        search_vector_unaccented_validated_project = SearchVector(
            Value(self.project_name, output_field=models.CharField()),
            weight="A",
            config="french_unaccent",
        ) + SearchVector(
            Value(self.description, output_field=models.CharField()),
            weight="B",
            config="french_unaccent",
        )

        self.search_vector_unaccented_validated_project = (
            search_vector_unaccented_validated_project
        )

    def save(self, *args, **kwargs):
        self.set_search_vector_unaccented_validated_project()
        return super().save(*args, **kwargs)
