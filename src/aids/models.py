from uuid import uuid4
from datetime import timedelta

from django.db import models
from django.db.models import Q, Value
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

from model_utils import Choices
from django_xworkflows import models as xwf_models

from aids.constants import (
    AUDIENCES_ALL,
    AID_TYPES_ALL,
    FINANCIAL_AIDS_LIST,
    TECHNICAL_AIDS_LIST,
)
from aids.tasks import send_publication_email
from core.fields import ChoiceArrayField, PercentRangeField
from dataproviders.constants import IMPORT_LICENCES


class AidWorkflow(xwf_models.Workflow):
    """Defines statuses and transitions for Aids."""

    log_model = ""

    states = Choices(
        ("draft", "Brouillon"),
        ("reviewable", "En revue"),
        ("published", "Publiée"),
        ("deleted", "Supprimée"),
        ("merged", "Fusionnée"),
    )
    initial_state = "draft"
    transitions = (
        ("submit", "draft", "reviewable"),
        ("publish", "reviewable", "published"),
        ("unpublish", ("reviewable", "published"), "draft"),
        ("soft_delete", ("draft", "reviewable", "published"), "deleted"),
    )


class AidQuerySet(models.QuerySet):
    """Custom queryset with additional filtering methods for aids."""

    def existing(self):
        """Exclude deleted aids."""

        return self.exclude(status=AidWorkflow.states.deleted.name)

    def deleted(self):
        """Only return deleted aids."""

        return self.filter(status=AidWorkflow.states.deleted.name)

    def published(self):
        """Only returns published objects."""

        return self.filter(status=AidWorkflow.states.published.name)

    def drafts(self):
        """Only return draft objects."""

        return self.filter(status=AidWorkflow.states.draft.name)

    def under_review(self):
        """Return aids that need to be review before publication."""

        return self.filter(status=AidWorkflow.states.reviewable.name)

    def open(self):
        """Returns aids that may appear in the search results (unexpired).

        An aid is considered open if:
          - the submission deadline is still in the future OR
          - the submission deadline is not provided OR
          - the recurrence field is set to "ongoing"
        """

        today = timezone.now().date()
        return self.filter(
            Q(submission_deadline__gte=today)
            | Q(submission_deadline__isnull=True)
            | Q(recurrence="ongoing")
        )

    def expired(self):
        """Returns expired aids. The opposite of the `open` filter."""

        today = timezone.now().date()
        return self.filter(Q(submission_deadline__lt=today) & ~Q(recurrence="ongoing"))

    def soon_expiring(self):
        """Returns aids that will expire soon."""

        today = timezone.now().date()
        soon = today + timedelta(days=settings.APPROACHING_DEADLINE_DELTA)
        return self.filter(
            Q(submission_deadline__gte=today)
            & Q(submission_deadline__lte=soon)
            & ~Q(recurrence="ongoing")
        )

    def hidden(self):
        """Returns the list of aids that do not appear on the frontend."""

        today = timezone.now().date()
        return self.filter(
            ~Q(status=AidWorkflow.states.published.name)
            | (Q(submission_deadline__lt=today) & ~Q(recurrence="ongoing"))
        )

    def live(self):
        """Returns the list of aids that appear on the frontend.

        An aid is considered live if:
          - the status is 'published'
          - the aid is open (see open())
        """
        return self.published().open()

    def has_projects(self):
        return self.filter(projects__isnull=False)

    def has_eligibility_test(self):
        """Only return aids with an eligibility test."""

        return self.filter(eligibility_test__isnull=False)

    def generic_aids(self):
        """Returns the list of generic aids."""

        return self.filter(is_generic=True)

    def local_aids(self):
        """Returns the list of local aids."""

        return self.filter(generic_aid__isnull=False)

    def standard_aids(self):
        """Returns the list of aids that are neither local nor generic."""

        return self.filter(generic_aid__isnull=True, is_generic=False)


class BaseExistingAidsManager(models.Manager):
    """Custom manager to only keep existing aids."""

    def get_queryset(self):
        qs = super().get_queryset().exclude(is_amendment=True).existing()
        return qs


ExistingAidsManager = BaseExistingAidsManager.from_queryset(AidQuerySet)


class BaseDeletedAidsManager(models.Manager):
    """Custom manager to only keep deleted aids."""

    def get_queryset(self):
        qs = super().get_queryset().exclude(is_amendment=True).deleted()
        return qs


DeletedAidsManager = BaseDeletedAidsManager.from_queryset(AidQuerySet)


class AmendmentManager(models.Manager):
    """Custom manager to only get amendments."""

    def get_queryset(self):
        qs = super().get_queryset().filter(is_amendment=True)
        return qs


class AidFinancer(models.Model):
    """The Aid -> Financers relationship `through` model."""

    aid = models.ForeignKey("aids.Aid", on_delete=models.CASCADE)
    backer = models.ForeignKey("backers.Backer", on_delete=models.CASCADE)
    order = models.PositiveIntegerField("Trier par", blank=False, default=1)

    class Meta:
        unique_together = ["aid", "backer"]
        ordering = ["order", "backer__name"]


class AidInstructor(models.Model):
    """The Aid -> Instructors relationship `through` model."""

    aid = models.ForeignKey("aids.Aid", on_delete=models.CASCADE)
    backer = models.ForeignKey("backers.Backer", on_delete=models.CASCADE)
    order = models.PositiveIntegerField("Trier par", blank=False, default=1)

    class Meta:
        unique_together = ["aid", "backer"]
        ordering = ["order", "backer__name"]


class Aid(xwf_models.WorkflowEnabled, models.Model):
    """Represents a single Aid."""

    TYPES = Choices(*AID_TYPES_ALL)

    STEPS = Choices(
        ("preop", "Réflexion / conception"),
        ("op", "Mise en œuvre / réalisation"),
        ("postop", "Usage / valorisation"),
    )

    EUROPEAN_AIDS = Choices(
        ("sectorial", "Sectorielle"),
        ("organizational", "Structurelle"),
    )

    AUDIENCES = Choices(*AUDIENCES_ALL)

    DESTINATIONS = Choices(
        ("supply", "Dépenses de fonctionnement"),
        ("investment", "Dépenses d’investissement"),
    )

    RECURRENCES = Choices(
        ("oneoff", "Ponctuelle"),
        ("ongoing", "Permanente"),
        ("recurring", "Récurrente"),
    )

    IS_CHARGED = (
        ("all", "Aides gratuites et payantes"),
        ("True", "Aides payantes"),
        ("False", "Aides gratuites"),
    )

    objects = ExistingAidsManager()
    all_aids = AidQuerySet.as_manager()
    deleted_aids = DeletedAidsManager()
    amendments = AmendmentManager()

    slug = models.SlugField(
        "Fragment d’URL", help_text="Laisser vide pour autoremplir.", blank=True
    )
    name = models.CharField(
        "Nom",
        max_length=180,
        help_text="Le titre doit commencer par un verbe à l’infinitif pour que l’objectif de l’aide soit explicite vis-à-vis de ses bénéficiaires.",  # noqa
        null=False,
        blank=False,
    )
    name_initial = models.CharField(
        "Nom initial",
        max_length=180,
        help_text="Comment cette aide s’intitule-t-elle au sein de votre structure ? Exemple : AAP Mob’Biodiv",  # noqa
        null=True,
        blank=True,
    )
    short_title = models.CharField(
        "Titre court",
        max_length=64,
        help_text="Un titre plus concis, pour affichage spécifique.",
        blank=True,
    )
    author = models.ForeignKey(
        "accounts.User",
        verbose_name="Auteur",
        on_delete=models.PROTECT,
        related_name="aids",
        help_text="Qui renseigne cette aide ?",
        null=True,
    )
    categories = models.ManyToManyField(
        "categories.Category",
        verbose_name="Sous-thématiques",
        related_name="aids",
        blank=True,
    )
    keywords = models.ManyToManyField(
        "keywords.Keyword",
        verbose_name="Mots clé",
        related_name="aids",
        blank=True,
    )
    financers = models.ManyToManyField(
        "backers.Backer",
        verbose_name="Porteurs d’aides",
        through=AidFinancer,
        related_name="financed_aids",
    )
    financer_suggestion = models.CharField(
        "Porteurs d'aides suggérés", max_length=256, blank=True
    )
    instructors = models.ManyToManyField(
        "backers.Backer",
        verbose_name="Instructeurs",
        through=AidInstructor,
        related_name="instructed_aids",
        blank=True,
    )
    instructor_suggestion = models.CharField(
        "Instructeurs suggérés", max_length=256, blank=True
    )
    description = models.TextField(
        "Description complète de l’aide et de ses objectifs", blank=False
    )
    project_examples = models.TextField(
        "Exemples de projets réalisables", default="", blank=True
    )
    projects = models.ManyToManyField(
        "projects.Project", through="AidProject", verbose_name="Projets", blank=True
    )
    suggested_projects = models.ManyToManyField(
        "projects.Project",
        through="SuggestedAidProject",
        related_name="suggested_aid",
        verbose_name="Projets suggérés",
        blank=True,
    )
    eligibility = models.TextField("Éligibilité", blank=True)
    perimeter = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="Périmètre",
        on_delete=models.PROTECT,
        help_text="Sur quel périmètre l’aide est-elle diffusée ?",
        null=True,
        blank=True,
    )
    perimeter_suggestion = models.CharField(
        "Périmètre suggéré", max_length=256, null=True, blank=True
    )
    mobilization_steps = ChoiceArrayField(
        verbose_name="État d’avancement du projet pour bénéficier du dispositif",
        null=True,
        blank=True,
        base_field=models.CharField(max_length=32, choices=STEPS, default=STEPS.preop),
    )
    origin_url = models.URLField("Plus d’informations", max_length=700, blank=True)
    application_url = models.URLField("Candidater à l’aide", max_length=700, blank=True)
    ds_schema_exists = models.BooleanField(
        "Schéma existant",
        help_text=(
            "Un schéma pour l’api de pré-remplissage"
            "de Démarches-Simplifiées est-il renseigné ?"
        ),
        default=False,
    )
    ds_id = models.PositiveIntegerField(
        "Identifiant de la démarche",
        help_text="Identifiant de la démarche sur Démarches-Simplifiées",
        null=True,
        blank=True,
    )
    ds_mapping = models.JSONField(
        "Mapping JSON de la démarche",
        help_text="Mapping JSON pour pré-remplissage sur Démarches-Simplifiées",
        editable=True,
        null=True,
        blank=True,
    )
    has_broken_link = models.BooleanField(
        "Contient un lien cassé ?",
        default=False,
    )
    targeted_audiences = ChoiceArrayField(
        verbose_name="Bénéficiaires de l’aide",
        null=True,
        blank=True,
        base_field=models.CharField(max_length=32, choices=AUDIENCES),
    )
    aid_types = ChoiceArrayField(
        verbose_name="Types d’aide",
        null=True,
        blank=True,
        base_field=models.CharField(max_length=32, choices=TYPES),
        help_text="Précisez le ou les types de l’aide.",
    )
    is_charged = models.BooleanField(
        "Aide Payante",
        help_text=(
            "Ne pas cocher pour les aides sous adhésion et ajouter la mention \
        « *sous adhésion » dans les critères d’éligibilité."
        ),
        default=False,
    )
    is_generic = models.BooleanField(
        "Aide générique ?", help_text="Cette aide est-elle générique ?", default=False
    )
    generic_aid = models.ForeignKey(
        "aids.Aid",
        verbose_name="Aide générique",
        on_delete=models.CASCADE,
        related_name="local_aids",
        limit_choices_to={"is_generic": True},
        help_text="Aide générique associée à une aide locale.",
        null=True,
        blank=True,
    )
    local_characteristics = models.TextField("Spécificités locales", blank=True)
    destinations = ChoiceArrayField(
        verbose_name="Types de dépenses / actions couvertes",
        help_text="Obligatoire pour les aides financières",
        null=True,
        blank=True,
        base_field=models.CharField(max_length=32, choices=DESTINATIONS),
    )
    start_date = models.DateField(
        "Date d’ouverture",
        help_text="À quelle date l’aide est-elle ouverte aux candidatures ?",
        null=True,
        blank=True,
    )
    predeposit_date = models.DateField(
        "Date de pré-dépôt",
        help_text="Quelle est la date de pré-dépôt des dossiers, si applicable ?",
        null=True,
        blank=True,
    )
    submission_deadline = models.DateField(
        "Date de clôture",
        help_text="Quelle est la date de clôture de dépôt des dossiers ?",
        null=True,
        blank=True,
    )
    subvention_rate = PercentRangeField(
        "Taux de subvention, min. et max. (en %, nombre entier)",
        help_text="Si le taux est fixe, remplissez uniquement le taux max.",
        null=True,
        blank=True,
    )
    subvention_comment = models.CharField(
        "Taux de subvention (commentaire optionnel)", max_length=255, blank=True
    )
    recoverable_advance_amount = models.PositiveIntegerField(
        "Montant de l’avance récupérable", null=True, blank=True
    )
    loan_amount = models.PositiveIntegerField(
        "Montant du prêt maximum", null=True, blank=True
    )
    other_financial_aid_comment = models.CharField(
        "Autre aide financière (commentaire optionnel)", max_length=100, blank=True
    )
    contact = models.TextField("Contact", blank=True)
    contact_email = models.EmailField("Adresse e-mail de contact", blank=True)
    contact_phone = models.CharField("Numéro de téléphone", max_length=35, blank=True)
    contact_detail = models.CharField("Contact (détail)", max_length=256, blank=True)
    recurrence = models.CharField(
        "Récurrence",
        help_text="L’aide est-elle ponctuelle, permanente, ou récurrente ?",
        max_length=16,
        choices=RECURRENCES,
        blank=True,
    )
    is_call_for_project = models.BooleanField(
        "Appel à projet / Manifestation d’intérêt", null=True
    )
    programs = models.ManyToManyField(
        "programs.Program", verbose_name="Programmes", related_name="aids", blank=True
    )
    status = xwf_models.StateField(AidWorkflow, verbose_name="Statut")

    # Eligibility
    eligibility_test = models.ForeignKey(
        "eligibility.EligibilityTest",
        verbose_name="Test d’éligibilité",
        on_delete=models.PROTECT,
        related_name="aids",
        null=True,
        blank=True,
    )

    # Dates
    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", default=timezone.now)
    date_published = models.DateTimeField(
        "Première date de publication", null=True, blank=True
    )

    # Specific to France Relance features
    in_france_relance = models.BooleanField(
        "France Relance ?",
        help_text="Cette aide est-elle éligible au programme France Relance ?",
        default=False,
    )

    # Specific to European features
    european_aid = models.CharField(
        verbose_name="Aide européenne ?",
        null=True,
        blank=False,
        default=None,
        max_length=32,
        choices=EUROPEAN_AIDS,
        help_text="Précisez si l’aide européenne est structurelle ou sectorielle",
    )

    # Disable send_publication_email's task
    author_notification = models.BooleanField(
        "Envoyer un email à l’auteur de l’aide ?",
        help_text="Un email doit-il être envoyé à l’auteur de cette aide \
        au moment de sa publication ?",
        default=True,
    )

    # Third-party data import related fields
    is_imported = models.BooleanField("Importé ?", default=False)
    import_data_source = models.ForeignKey(
        "dataproviders.DataSource",
        verbose_name="Source de données",
        on_delete=models.PROTECT,
        related_name="aids",
        null=True,
    )
    # Even if this field is a CharField, we make it nullable with `null=True`
    # because null values are not taken into account by postgresql when
    # enforcing the `unique` constraint, which is very handy for us.
    import_uniqueid = models.CharField(
        "Identifiant d’import unique",
        max_length=200,
        unique=True,
        null=True,
        blank=True,
    )
    import_data_url = models.URLField(
        "URL d’origine de la donnée importée", null=True, blank=True
    )
    import_share_licence = models.CharField(
        "Sous quelle licence cette aide a-t-elle été partagée ?",
        max_length=50,
        choices=IMPORT_LICENCES,
        blank=True,
    )
    import_data_mention = models.CharField(
        "Mention du partenariat avec le propriétaire de la donnée",
        max_length=900,
        null=True,
        blank=True,
    )
    import_last_access = models.DateField(
        "Date du dernier accès", null=True, blank=True
    )
    import_updated = models.BooleanField(
        "En attente de revue des données importées mises à jour",
        help_text=(
            "Cette aide est en attente d’une revue des mises à jour \
        proposées par l’outil d’import"
        ),
        default=False,
    )
    import_raw_object = models.JSONField("Donnée JSON brute", editable=False, null=True)
    import_raw_object_calendar = models.JSONField(
        "Donnée JSON brute du calendrier", editable=False, null=True
    )
    import_raw_object_temp = models.JSONField(
        "Donnée JSON brute temporaire", editable=False, null=True
    )
    import_raw_object_temp_calendar = models.JSONField(
        "Donnée JSON brute temporaire du calendrier", editable=False, null=True
    )

    contact_info_updated = models.BooleanField(
        "En attente de revue des données de contact mises à jour",
        help_text=(
            "Cette aide est en attente d’une revue des données \
                de contact"
        ),
        default=False,
    )

    # This field is used to index searchable text content
    search_vector_unaccented = SearchVectorField("Search vector unaccented", null=True)

    # Those fields handle the "aid amendment" feature
    # Users, including anonymous, can suggest amendments to existing aids.
    # We store a suggested edit as a clone of the original aid, with the
    # following field as True.
    is_amendment = models.BooleanField("Est un amendement", default=False)
    amended_aid = models.ForeignKey(
        "aids.Aid", verbose_name="Aide amendée", on_delete=models.CASCADE, null=True
    )
    amendment_author_name = models.CharField(
        "Auteur de l’amendement", max_length=256, blank=True
    )
    amendment_author_email = models.EmailField(
        "E-mail de l’auteur de l’amendement", null=True, blank=True
    )
    amendment_author_org = models.CharField(
        "Structure de l’auteur de l’amendement", max_length=255, blank=True
    )
    amendment_comment = models.TextField("Commentaire", blank=True)

    class Meta:
        verbose_name = "Aide"
        verbose_name_plural = "Aides"
        indexes = [
            GinIndex(fields=["search_vector_unaccented"]),
        ]
        ordering = ["-id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We store here the current status as we need to check if it
        # has change - check what we do when saving the Aid instance.
        self.original_status = self.status

    def set_slug(self):
        """Set the object's slug.

        Lots of aids have duplicate name, so we prefix the slug with random
        characters."""
        if not self.id:
            full_title = "{}-{}".format(str(uuid4())[:4], self.name)
            self.slug = slugify(full_title)[:50]

    def set_publication_date(self):
        """Set the object's publication date.

        We set the first publication date once and for all when the aid is
        first published.
        """
        if self.is_published() and self.date_published is None:
            self.date_published = timezone.now()

    def set_search_vector_unaccented(
        self,
        financers=None,
        instructors=None,
        categories=None,
        keywords=None,
        programs=None,
    ):
        """Update the full text unaccented cache field."""

        # Note: we use `SearchVector(Value(self.field))` instead of
        # `SearchVector('field')` because the latter only works for updates,
        # not when inserting new records.
        #
        # Note 2: we have to pass the financers parameter instead of using
        # `self.financers.all()` because that last expression would not work
        # during an object creation.
        search_vector_unaccented = (
            SearchVector(
                Value(self.name, output_field=models.CharField()),
                weight="A",
                config="french_unaccent",
            )
            + SearchVector(
                Value(self.name_initial, output_field=models.CharField()),
                weight="A",
                config="french_unaccent",
            )
            + SearchVector(
                Value(self.short_title, output_field=models.CharField()),
                weight="A",
                config="french_unaccent",
            )
            + SearchVector(
                Value(self.description, output_field=models.CharField()),
                weight="B",
                config="french_unaccent",
            )
            + SearchVector(
                Value(self.project_examples, output_field=models.CharField()),
                weight="D",
                config="french_unaccent",
            )
            + SearchVector(
                Value(self.eligibility, output_field=models.CharField()),
                weight="D",
                config="french_unaccent",
            )
        )

        if categories:
            search_vector_unaccented += SearchVector(
                Value(
                    " ".join(str(category) for category in categories),
                    output_field=models.CharField(),
                ),
                weight="A",
                config="french_unaccent",
            )

        if keywords:
            search_vector_unaccented += SearchVector(
                Value(
                    " ".join(str(keyword) for keyword in keywords),
                    output_field=models.CharField(),
                ),
                weight="C",
                config="french_unaccent",
            )

        if programs:
            search_vector_unaccented += SearchVector(
                Value(
                    " ".join(str(program) for program in programs),
                    output_field=models.CharField(),
                ),
                weight="A",
                config="french_unaccent",
            )

        if financers:
            search_vector_unaccented += SearchVector(
                Value(
                    " ".join(str(backer) for backer in financers),
                    output_field=models.CharField(),
                ),
                weight="D",
                config="french_unaccent",
            )

        if instructors:
            search_vector_unaccented += SearchVector(
                Value(
                    " ".join(str(backer) for backer in instructors),
                    output_field=models.CharField(),
                ),
                weight="D",
                config="french_unaccent",
            )

        self.search_vector_unaccented = search_vector_unaccented

    def save(self, *args, **kwargs):
        self.set_slug()
        self.set_publication_date()
        is_new = not self.id  # There's no ID => newly created aid
        is_being_published = self.is_published() and self.status_has_changed()
        if (
            not is_new
            and is_being_published
            and self.author_notification
            and not self.is_imported
        ):
            send_publication_email.delay(aid_id=self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("aid_detail_view", args=[self.slug])

    def get_admin_url(self):
        return reverse("admin:aids_aid_change", args=[self.id])

    def get_sorted_local_aids(self):
        return (
            self.local_aids.live()
            .select_related("perimeter")
            .order_by("perimeter__name")
        )

    def is_draft(self):
        return self.status == AidWorkflow.states.draft

    def is_under_review(self):
        return self.status == AidWorkflow.states.reviewable

    def is_published(self):
        return self.status == AidWorkflow.states.published

    def status_has_changed(self):
        return self.original_status != self.status

    def is_financial(self):
        """Does this aid have financial parts?"""
        aid_types = self.aid_types or []
        return bool(set(aid_types) & set(FINANCIAL_AIDS_LIST))

    def is_grant(self):
        """Does this aid is a grant?"""
        aid_types = self.aid_types or []
        return bool(set(aid_types) & set((("grant", "Subvention"))))

    def is_loan(self):
        """Does this aid is a loan?"""
        aid_types = self.aid_types or []
        return bool(set(aid_types) & set((("loan", "Prêt"))))

    def is_technical(self):
        """Does this aid have technical parts?"""
        aid_types = self.aid_types or []
        return bool(set(aid_types) & set(TECHNICAL_AIDS_LIST))

    def is_recurring(self):
        return self.recurrence == self.RECURRENCES.recurring

    def is_ongoing(self):
        return self.recurrence == self.RECURRENCES.ongoing

    def has_calendar(self):
        """Does the aid has valid calendar data?."""

        if self.is_ongoing():
            return False

        return any((self.start_date, self.predeposit_date, self.submission_deadline))

    def has_approaching_deadline(self):
        if self.is_ongoing() or not self.submission_deadline:
            return False

        delta = self.submission_deadline - timezone.now().date()
        return delta.days >= 0 and delta.days <= settings.APPROACHING_DEADLINE_DELTA

    def days_before_deadline(self):
        if not self.submission_deadline or self.is_ongoing():
            return None

        today = timezone.now().date()
        deadline_delta = self.submission_deadline - today
        return deadline_delta.days

    def is_coming_soon(self):
        if not self.start_date:
            return False

        today = timezone.now().date()
        return self.start_date > today

    def has_expired(self):
        if not self.submission_deadline:
            return False

        today = timezone.now().date()
        return self.submission_deadline < today

    def is_live(self):
        """True if the aid must be displayed on the site."""
        return self.is_published() and not self.has_expired()

    def has_projects(self):
        return self.projects is not None

    def get_live_status_display(self):
        status = "Affichée" if self.is_live() else "Non affichée"
        return status

    def has_eligibility_test(self):
        return self.eligibility_test is not None

    def is_local(self):
        return self.generic_aid is not None

    def is_corporate_aid(self):
        return (
            self.targeted_audiences
            and self.AUDIENCES.private_sector in self.targeted_audiences
        )

    def clone_m2m(self, source_aid):
        """
        Clones the many-to-many fields for the the given source aid.
        """
        m2m_fields = self._meta.many_to_many
        projects_field = self._meta.get_field("projects")
        suggest_projects_field = self._meta.get_field("suggested_projects")

        for field in m2m_fields:
            if field != projects_field or field != suggest_projects_field:
                for item in field.value_from_object(source_aid):
                    getattr(self, field.attname).add(item)
        self.save()


class AidProject(models.Model):
    aid = models.ForeignKey(
        "Aid", on_delete=models.CASCADE, verbose_name="Aide", blank=True
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        verbose_name="Projet",
        blank=True,
    )
    creator = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        verbose_name="Créateur",
        blank=True,
        null=True,
    )
    aid_requested = models.BooleanField(
        "Aide demandée ?",
        help_text="Cette aide a-t-elle été demandée par le porteur du projet ?",
        default=False,
    )
    aid_obtained = models.BooleanField(
        "Aide obtenue ?",
        help_text="Cette aide a-t-elle été obtenue par le porteur du projet ?",
        default=False,
    )
    aid_denied = models.BooleanField(
        "Aide refusée ?",
        help_text="Cette aide a-t-elle été refusée au porteur du projet ?",
        default=False,
    )
    date_requested = models.DateTimeField(
        "Date de la demande",
        help_text="Date à laquelle cette aide a été demandée par le porteur du projet",
        null=True,
        blank=True,
    )
    aid_paid = models.BooleanField(
        "Aide reçue ?",
        help_text="Cette aide a-t-elle été reçue par le porteur du projet ?",
        default=False,
    )
    date_obtained = models.DateTimeField(
        "Date de l’obtention",
        help_text="Date à laquelle cette aide a été obtenue par le porteur du projet",
        null=True,
        blank=True,
    )
    date_denied = models.DateTimeField(
        "Date du refus",
        help_text="Date à laquelle cette aide a été refusée au porteur du projet",
        null=True,
        blank=True,
    )
    date_paid = models.DateTimeField(
        "Date de la réception de l’aide",
        help_text="Date à laquelle cette aide a été reçue par le porteur du projet",
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField("Date de création", default=timezone.now)


class SuggestedAidProject(models.Model):
    aid = models.ForeignKey(
        "Aid", on_delete=models.CASCADE, verbose_name="Aide suggérée", blank=True
    )
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, verbose_name="Projet", blank=True
    )
    creator = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        verbose_name="Créateur",
        blank=True,
        null=True,
    )
    is_associated = models.BooleanField(
        "Aide associée ?",
        help_text="Cette aide a-t-elle été acceptée par le porteur du projet ?",
        default=False,
    )
    is_rejected = models.BooleanField(
        "Aide rejetée ?",
        help_text="Cette aide a-t-elle été rejetée par le porteur du projet ?",
        default=False,
    )
    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_associated = models.DateTimeField(
        "Date d’association",
        help_text="Date à laquelle cette aide a été acceptée par le porteur du projet",
        null=True,
        blank=True,
    )
    date_rejected = models.DateTimeField(
        "Date de rejet",
        help_text="Date à laquelle cette aide a été rejetée par le porteur du projet",
        null=True,
        blank=True,
    )
