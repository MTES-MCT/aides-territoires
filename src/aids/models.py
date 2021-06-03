from uuid import uuid4
from datetime import timedelta

from django.db import models
from django.db.models import Q, Value
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

from model_utils import Choices
from django_xworkflows import models as xwf_models

from aids.tasks import send_publication_email
from core.fields import ChoiceArrayField, PercentRangeField
from tags.models import Tag
from dataproviders.constants import IMPORT_LICENCES


class AidWorkflow(xwf_models.Workflow):
    """Defines statuses and transitions for Aids."""

    log_model = ''

    states = Choices(
        ('draft', _('Draft')),
        ('reviewable', _('Under review')),
        ('published', pgettext_lazy('Aid (nf)', 'Published')),
        ('deleted', pgettext_lazy('Aid (nf)', 'Deleted')),
    )
    initial_state = 'draft'
    transitions = (
        ('submit', 'draft', 'reviewable'),
        ('publish', 'reviewable', 'published'),
        ('unpublish', ('reviewable', 'published'), 'draft'),
        ('soft_delete', ('draft', 'reviewable', 'published'), 'deleted')
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
            | Q(recurrence='ongoing'))

    def expired(self):
        """Returns expired aids. The opposite of the `open` filter."""

        today = timezone.now().date()
        return self.filter(
            Q(submission_deadline__lt=today)
            & ~Q(recurrence='ongoing'))

    def soon_expiring(self):
        """Returns aids that will expire soon."""

        today = timezone.now().date()
        soon = today + timedelta(days=settings.APPROACHING_DEADLINE_DELTA)
        return self.filter(
            Q(submission_deadline__gte=today)
            & Q(submission_deadline__lte=soon)
            & ~Q(recurrence='ongoing'))

    def hidden(self):
        """Returns the list of aids that do not appear on the frontend."""

        today = timezone.now().date()
        return self.filter(
            ~Q(status=AidWorkflow.states.published.name)
            | (
                Q(submission_deadline__lt=today)
                & ~Q(recurrence='ongoing')))

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
        """Returns the list of generic aids"""

        return self.filter(is_generic=True)

    def local_aids(self):
        """Returns the list of local aids"""

        return self.filter(generic_aid__isnull=False)

    def standard_aids(self):
        """Returns the list of aids that are nither local nor generic"""

        return self.filter(generic_aid__isnull=True, is_generic=False)


class BaseExistingAidsManager(models.Manager):
    """Custom manager to only keep existing aids."""

    def get_queryset(self):
        qs = super().get_queryset() \
            .exclude(is_amendment=True) \
            .existing()
        return qs


ExistingAidsManager = BaseExistingAidsManager.from_queryset(AidQuerySet)


class BaseDeletedAidsManager(models.Manager):
    """Custom manager to only keep deleted aids."""

    def get_queryset(self):
        qs = super().get_queryset() \
            .exclude(is_amendment=True) \
            .deleted()
        return qs


DeletedAidsManager = BaseDeletedAidsManager.from_queryset(AidQuerySet)


class AmendmentManager(models.Manager):
    """Custom manager to only get amendments."""

    def get_queryset(self):
        qs = super().get_queryset() \
            .filter(is_amendment=True)
        return qs


class AidFinancer(models.Model):
    """The Aid -> Financers relationship `through` model."""

    aid = models.ForeignKey('aids.Aid', on_delete=models.CASCADE)
    backer = models.ForeignKey('backers.Backer', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(
        _('Order'),
        blank=False,
        default=1)

    class Meta:
        unique_together = ['aid', 'backer']
        ordering = ['order', 'backer__name']


class AidInstructor(models.Model):
    """The Aid -> Instructors relationship `through` model."""

    aid = models.ForeignKey('aids.Aid', on_delete=models.CASCADE)
    backer = models.ForeignKey('backers.Backer', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(
        _('Order'),
        blank=False,
        default=1)

    class Meta:
        unique_together = ['aid', 'backer']
        ordering = ['order', 'backer__name']


class Aid(xwf_models.WorkflowEnabled, models.Model):
    """Represents a single Aid."""

    TYPES = Choices(
        ('grant', _('Grant')),
        ('loan', _('Loan')),
        ('recoverable_advance', _('Recoverable advance')),
        ('technical', _('Technical engineering')),
        ('financial', _('Financial engineering')),
        ('legal', _('Legal engineering')),
        ('other', _('Other')),
    )

    FINANCIAL_AIDS = ('grant', 'loan', 'recoverable_advance',
                      'other')

    TECHNICAL_AIDS = ('technical', 'financial', 'legal')

    PERIMETERS = Choices(
        ('europe', _('Europe')),
        ('france', _('France')),
        ('region', _('Region')),
        ('department', _('Department')),
        ('commune', _('Commune')),
        ('mainland', _('Mainland')),
        ('overseas', _('Overseas')),
        ('other', _('Other')),
    )

    STEPS = Choices(
        ('preop', _('Preoperational')),
        ('op', _('Operational')),
        ('postop', _('Postoperation')),
    )

    AUDIENCES = Choices(
        ('commune', _('Communes')),
        ('epci', _('Audience EPCI')),
        ('department', _('Departments')),
        ('region', _('Regions')),
        ('association', _('Associations')),
        ('private_sector', _('Private sector')),
        ('public_cies', _('Local public companies')),
        ('public_org', _('Public organization')),
        ('researcher', _('Research')),
        ('private_person', _('Individuals')),
        ('farmer', _('Farmers')),
        ('special', _('Special status for outre-mer')),
    )

    DESTINATIONS = Choices(
        ('supply', _('Supply')),
        ('investment', _('Investment')),
    )

    RECURRENCE = Choices(
        ('oneoff', _('One off')),
        ('ongoing', _('Ongoing')),
        ('recurring', _('Recurring')),
    )

    objects = ExistingAidsManager()
    all_aids = AidQuerySet.as_manager()
    deleted_aids = DeletedAidsManager()
    amendments = AmendmentManager()

    slug = models.SlugField(
        _('Slug'),
        help_text=_('Let it empty so it will be autopopulated.'),
        blank=True)
    name = models.CharField(
        _('Name'),
        max_length=180,
        help_text=_('Use an infinitive form to make the aid\'s purpose clear'),
        null=False, blank=False)
    short_title = models.CharField(
        _('Short title'),
        max_length=64,
        help_text=_('A shorter, more concise title'),
        blank=True)
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        related_name='aids',
        help_text=_('Who is submitting the aid?'),
        null=True)
    categories = models.ManyToManyField(
        'categories.Category',
        verbose_name=_('Categories'),
        related_name='aids',
        blank=True)
    financers = models.ManyToManyField(
        'backers.Backer',
        through=AidFinancer,
        related_name='financed_aids',
        verbose_name=_('Financers'))
    financer_suggestion = models.CharField(
        _('Financer suggestion'),
        max_length=256,
        blank=True)
    instructors = models.ManyToManyField(
        'backers.Backer',
        through=AidInstructor,
        blank=True,
        related_name='instructed_aids',
        verbose_name=_('Instructors'))
    instructor_suggestion = models.CharField(
        _('Instructor suggestion'),
        max_length=256,
        blank=True)
    description = models.TextField(
        _('Full description of the aid and its objectives'),
        blank=False)
    project_examples = models.TextField(
        _('Project examples'),
        default='',
        blank=True)
    projects = models.ManyToManyField(
        'projects.Project',
        verbose_name=_('Projects'),
        related_name='aids',
        blank=True)
    eligibility = models.TextField(
        _('Eligibility'),
        blank=True)
    perimeter = models.ForeignKey(
        'geofr.Perimeter',
        verbose_name=_('Perimeter'),
        on_delete=models.PROTECT,
        null=True, blank=True,
        help_text=_('What is the aid broadcasting perimeter?'))
    perimeter_suggestion = models.CharField(
        _('Perimeter suggestion'),
        max_length=256,
        null=True, blank=True)
    mobilization_steps = ChoiceArrayField(
        verbose_name=_('Mobilization step'),
        null=True, blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=STEPS,
            default=STEPS.preop))
    origin_url = models.URLField(
        _('Origin URL'),
        max_length=500,
        blank=True)
    application_url = models.URLField(
        _('Application url'),
        max_length=500,
        blank=True)
    targeted_audiences = ChoiceArrayField(
        verbose_name=_('Targeted audiences'),
        null=True, blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=AUDIENCES))
    aid_types = ChoiceArrayField(
        verbose_name=_('Aid types'),
        null=True, blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=TYPES),
        help_text=_('Specify the aid type or types.'))
    is_generic = models.BooleanField(_('Is generic aid'), default=False)
    generic_aid = models.ForeignKey(
        'aids.Aid',
        verbose_name=_('Generic aid'),
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='local_aids',
        limit_choices_to={'is_generic': True},
        help_text=_("Generic aid associated to a local aid"))
    local_characteristics = models.TextField(
        _('Local characteristics'),
        blank=True)
    destinations = ChoiceArrayField(
        verbose_name=_('Destinations'),
        null=True,
        blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=DESTINATIONS))
    start_date = models.DateField(
        _('Start date'),
        null=True, blank=True,
        help_text=_('When is the application opening?'))
    predeposit_date = models.DateField(
        _('Predeposit date'),
        null=True, blank=True,
        help_text=_('When is the pre-deposit date, if applicable?'))
    submission_deadline = models.DateField(
        _('Submission deadline'),
        null=True, blank=True,
        help_text=_('When is the submission deadline?'))
    subvention_rate = PercentRangeField(
        _('Subvention rate, min. and max. (in round %)'),
        null=True, blank=True,
        help_text=_('If fixed rate, only fill the max. rate.'))
    subvention_comment = models.CharField(
        _('Subvention rate, optional comment'),
        max_length=100,
        blank=True)
    contact = models.TextField(
        _('Contact'),
        blank=True)
    contact_email = models.EmailField(
        _('Contact email'),
        blank=True)
    contact_phone = models.CharField(
        _('Contact phone number'),
        max_length=35,
        blank=True)
    contact_detail = models.CharField(
        _('Contact detail'),
        max_length=256,
        blank=True)
    recurrence = models.CharField(
        _('Recurrence'),
        help_text=_('Is this a one-off aid, is it recurring or ongoing?'),
        max_length=16,
        choices=RECURRENCE,
        blank=True)
    is_call_for_project = models.BooleanField(
        _('Call for project / Call for expressions of interest'),
        null=True)
    programs = models.ManyToManyField(
        'programs.Program',
        related_name='aids',
        verbose_name=_('Programs'),
        blank=True)
    status = xwf_models.StateField(
        AidWorkflow,
        verbose_name=_('Status'))

    # Eligibility
    eligibility_test = models.ForeignKey(
        'eligibility.EligibilityTest',
        on_delete=models.PROTECT,
        verbose_name=_('Eligibility test'),
        related_name='aids',
        null=True, blank=True)

    # Dates
    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)
    date_updated = models.DateTimeField(
        _('Date updated'),
        auto_now=True)
    date_published = models.DateTimeField(
        _('First publication date'),
        null=True, blank=True)

    # Specific to France Relance features
    in_france_relance = models.BooleanField(
        _('France Relance?'),
        default=False,
        help_text=_('Is this aid a part of the France Relance program?'))

    # Third-party data import related fields
    is_imported = models.BooleanField(
        _('Is imported?'),
        default=False)
    import_data_source = models.ForeignKey(
        'dataproviders.DataSource',
        verbose_name=_('Data Source'),
        related_name='aids',
        on_delete=models.PROTECT,
        null=True)
    # Even if this field is a CharField, we make it nullable with `null=True`
    # because null values are not taken into account by postgresql when
    # enforcing the `unique` constraint, which is very handy for us.
    import_uniqueid = models.CharField(
        _('Unique identifier for imported data'),
        max_length=200,
        unique=True,
        null=True, blank=True)
    import_data_url = models.URLField(
        _('Origin url of the imported data'),
        null=True, blank=True)
    import_share_licence = models.CharField(
        _('Under which license was this aid shared?'),
        max_length=50,
        choices=IMPORT_LICENCES,
        blank=True)
    import_last_access = models.DateField(
        _('Date of the latest access'),
        null=True, blank=True)
    import_raw_object = models.JSONField(null=True)

    # This field is used to index searchable text content
    search_vector = SearchVectorField(
        _('Search vector'),
        null=True)

    # This is where we store tags
    tags = ArrayField(
        models.CharField(max_length=50, blank=True),
        verbose_name=_('Tags'),
        default=list,
        size=30,
        blank=True)
    _tags_m2m = models.ManyToManyField(
        'tags.Tag',
        related_name='aids',
        verbose_name=_('Tags'))

    # Those fields handle the "aid amendment" feature
    # Users, including anonymous, can suggest amendments to existing aids.
    # We store a suggested edit as a clone of the original aid, with the
    # following field as True.
    is_amendment = models.BooleanField(
        _('Is amendment'),
        default=False)
    amended_aid = models.ForeignKey(
        'aids.Aid',
        verbose_name=_('Amended aid'),
        on_delete=models.CASCADE,
        null=True)
    amendment_author_name = models.CharField(
        _('Amendment author'),
        max_length=256,
        blank=True)
    amendment_author_email = models.EmailField(
        _('Amendment author email'),
        null=True, blank=True)
    amendment_author_org = models.CharField(
        _('Amendment author organization'),
        max_length=255,
        blank=True)
    amendment_comment = models.TextField(
        _('Amendment comment'),
        blank=True)

    class Meta:
        verbose_name = _('Aid')
        verbose_name_plural = _('Aids')
        indexes = [
            GinIndex(fields=['search_vector']),
        ]

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
            full_title = '{}-{}'.format(str(uuid4())[:4], self.name)
            self.slug = slugify(full_title)[:50]

    def set_publication_date(self):
        """Set the object's publication date.

        We set the first publication date once and for all when the aid is
        first published.
        """
        if self.is_published() and self.date_published is None:
            self.date_published = timezone.now()

    def set_search_vector(self, financers=None, instructors=None):
        """Update the full text cache field."""

        # Note: we use `SearchVector(Value(self.field))` instead of
        # `SearchVector('field')` because the latter only works for updates,
        # not when inserting new records.
        #
        # Note 2: we have to pass the financers parameter instead of using
        # `self.financers.all()` because that last expression would not work
        # during an object creation.
        search_vector = \
            SearchVector(
                Value(self.name, output_field=models.CharField()),
                weight='A',
                config='french') + \
            SearchVector(
                Value(self.eligibility, output_field=models.CharField()),
                weight='D',
                config='french') + \
            SearchVector(
                Value(self.description, output_field=models.CharField()),
                weight='B',
                config='french') + \
            SearchVector(
                Value(' '.join(self.tags), output_field=models.CharField()),
                weight='A',
                config='french')

        if financers:
            search_vector += SearchVector(
                Value(
                    ' '.join(str(backer) for backer in financers),
                    output_field=models.CharField()),
                weight='D',
                config='french')

        if instructors:
            search_vector += SearchVector(
                Value(
                    ' '.join(str(backer) for backer in instructors),
                    output_field=models.CharField()),
                weight='D',
                config='french')

        self.search_vector = search_vector

    def populate_tags(self):
        """Populates the `_tags_m2m` field.

        cache `_tags_m2m` field with values from the `tags` field.

        Tag that do not exist will be created.
        """
        all_tag_names = self.tags
        existing_tag_objects = Tag.objects.filter(name__in=all_tag_names)
        existing_tag_names = [tag.name for tag in existing_tag_objects]
        missing_tag_names = list(set(all_tag_names) - set(existing_tag_names))
        new_tags = [Tag(name=tag) for tag in missing_tag_names]
        new_tag_objects = Tag.objects.bulk_create(new_tags)

        all_tag_objects = list(existing_tag_objects) + list(new_tag_objects)
        self._tags_m2m.set(all_tag_objects, clear=True)

    def save(self, *args, **kwargs):
        self.set_slug()
        self.set_publication_date()
        is_new = not self.id  # There's no ID => newly created aid
        is_being_published = self.is_published() and self.status_has_changed()
        if not is_new and is_being_published and not self.is_imported:
            send_publication_email.delay(aid_id=self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('aid_detail_view', args=[self.slug])

    def get_admin_url(self):
        return reverse('admin:aids_aid_change', args=[self.id])

    def get_sorted_local_aids(self):
        return self.local_aids.order_by('perimeter__name')

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
        return bool(set(aid_types) & set(self.FINANCIAL_AIDS))

    def is_technical(self):
        """Does this aid have technical parts?"""
        aid_types = self.aid_types or []
        return bool(set(aid_types) & set(self.TECHNICAL_AIDS))

    def is_ongoing(self):
        return self.recurrence == self.RECURRENCE.ongoing

    def has_calendar(self):
        """Does the aid has valid calendar data?."""

        if self.is_ongoing():
            return False

        return any((
            self.start_date,
            self.predeposit_date,
            self.submission_deadline))

    def has_approaching_deadline(self):
        if self.is_ongoing() or not self.submission_deadline:
            return False

        delta = self.submission_deadline - timezone.now().date()
        return delta.days >= 0 \
            and delta.days <= settings.APPROACHING_DEADLINE_DELTA

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
        status = _('Displayed') if self.is_live() else _('Not displayed')
        return status

    def has_eligibility_test(self):
        return self.eligibility_test is not None

    def is_local(self):
        return self.generic_aid is not None

    def is_corporate_aid(self):
        return (
            self.targeted_audiences and
            'private_sector' in self.targeted_audiences)
