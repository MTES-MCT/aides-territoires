from uuid import uuid4

from django.db import models
from django.db.models import Q, Value
from django.contrib.postgres.fields import ArrayField, IntegerRangeField
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

from model_utils import Choices
from django_xworkflows import models as xwf_models

from core.fields import ChoiceArrayField, PercentRangeField
from tags.models import Tag


class AidQuerySet(models.QuerySet):
    """Custom queryset with additional filtering methods for aids."""

    def published(self):
        """Only returns published objects."""

        return self.filter(status='published')

    def drafts(self):
        """Only return draft objects."""

        return self.filter(status='draft')

    def under_review(self):
        """Return aids that need to be review before publication."""

        return self.filter(status='reviewable')

    def open(self):
        """Returns aids that may appear in the search results (unexpired)."""

        today = timezone.now().date()
        return self.filter(
            Q(submission_deadline__gte=today)
            | Q(submission_deadline__isnull=True))


class BaseAidManager(models.Manager):
    """Custom manager to only keep existing aids."""

    def get_queryset(self):
        qs = super().get_queryset() \
            .exclude(status='deleted') \
            .exclude(is_amendment=True)
        return qs


ExistingAidsManager = BaseAidManager.from_queryset(AidQuerySet)


class AmendmentManager(models.Manager):
    """Custom manager to only get amendments."""

    def get_queryset(self):
        qs = super().get_queryset() \
            .filter(is_amendment=True)
        return qs


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
    transitions = (('submit', 'draft', 'reviewable'), ('publish', 'reviewable',
                                                       'published'),
                   ('unpublish', ('reviewable', 'published'),
                    'draft'), ('soft_delete', ('draft', 'reviewable',
                                               'published'), 'deleted'))


class Aid(xwf_models.WorkflowEnabled, models.Model):
    """Represents a single Aid."""

    TYPES = Choices(
        ('grant', _('Grant')),
        ('loan', _('Loan')),
        ('recoverable_advance', _('Recoverable advance')),
        ('technical', _('Technical')),
        ('financial', _('Financial')),
        ('legal', _('Legal')),
        ('other', _('Other')),
    )

    FINANCIAL_AIDS = ('grant', 'loan', 'recoverable_advance',
                      'interest_subsidy')

    TECHNICAL_AIDS = ('guidance', 'networking', 'valorisation')

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

    AUDIANCES = Choices(
        ('commune', _('Commune')),
        ('epci', _('Audiance EPCI')),
        ('department', _('Department')),
        ('region', _('Region')),
        ('association', _('Association')),
        ('private_sector', _('Private sector')),
        ('public_org', _('Public organization')),
        ('lessor', _('Audiance lessor')),
        ('researcher', _('Research')),
        ('private_person', _('Individual')),
        ('other', _('Other')),
    )

    DESTINATIONS = Choices(
        ('service', _('Service (AMO, survey)')),
        ('works', _('Works')),
        ('supply', _('Supply')),
    )

    RECURRENCE = Choices(
        ('oneoff', _('One off')),
        ('ongoing', _('Ongoing')),
        ('recurring', _('Recurring')),
    )

    IMPORT_LICENCES = Choices(
        ('unknown', _('Unknown')),
        ('openlicence20', _('Open licence 2.0')),
    )

    objects = ExistingAidsManager()
    all_aids = AidQuerySet.as_manager()
    amendments = AmendmentManager()

    slug = models.SlugField(
        _('Slug'),
        help_text=_('Let it empty so it will be autopopulated.'),
        blank=True)
    name = models.CharField(
        _('Name'),
        max_length=180,
        help_text=_('A good title describes the purpose of the help and '
                    'should speak to the recipient.'),
        null=False, blank=False)
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        help_text=_('Who is submitting the aid?'),
        null=True)
    backers = models.ManyToManyField(
        'backers.Backer',
        related_name='aids',
        verbose_name=_('Backers'),
        help_text=_('On a national level if appropriate'))
    new_backer = models.CharField(
        _('New backer'),
        max_length=256,
        blank=True)
    description = models.TextField(
        _('Short description'),
        blank=False)
    eligibility = models.TextField(
        _('Eligibility'),
        blank=True)
    perimeter = models.ForeignKey(
        'geofr.Perimeter',
        verbose_name=_('Perimeter'),
        on_delete=models.PROTECT,
        null=True, blank=True,
        help_text=_('What is the aid broadcasting perimeter?'))
    mobilization_steps = ChoiceArrayField(
        verbose_name=_('Mobilization step'),
        null=True, blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=STEPS,
            default=STEPS.preop))
    origin_url = models.URLField(
        _('Origin URL'),
        blank=True)
    application_url = models.URLField(
        _('Application url'),
        blank=True)
    targeted_audiances = ChoiceArrayField(
        verbose_name=_('Targeted audiances'),
        null=True, blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=AUDIANCES))
    aid_types = ChoiceArrayField(
        verbose_name=_('Aid types'),
        null=True, blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=TYPES),
        help_text=_('Specify the aid type or types.'))
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
        max_length=256,
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
        null=True, blank=True)
    status = xwf_models.StateField(
        AidWorkflow,
        verbose_name=_('Status'))
    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)
    date_updated = models.DateTimeField(
        _('Date updated'),
        auto_now=True)
    date_published = models.DateTimeField(
        _('First publication date'),
        null=True, blank=True)

    # Third-party data import related fields
    is_imported = models.BooleanField(
        _('Is imported?'),
        default=False)
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

    def set_search_vector(self, backers):
        """Update the full text cache field."""

        # Note: we use `SearchVector(Value(self.field))` instead of
        # `SearchVector('field')` because the latter only works for updates,
        # not when inserting new records.
        #
        # Note 2: we have to pass the backers parameter instead of using
        # `self.backers.all()` because that last expression would not work
        # during an object creation.
        self.search_vector = \
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
                config='french') + \
            SearchVector(
                Value(
                    ' '.join(str(backer) for backer in backers),
                    output_field=models.CharField()),
                weight='D',
                config='french')

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
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('aid_detail_view', args=[self.slug])

    def get_admin_url(self):
        return reverse('admin:aids_aid_change', args=[self.id])

    def is_draft(self):
        return self.status == AidWorkflow.states.draft

    def is_under_review(self):
        return self.status == AidWorkflow.states.reviewable

    def is_published(self):
        return self.status == AidWorkflow.states.published

    def is_financial(self):
        """Does this aid have financial parts?"""
        aid_types = self.aid_types or []
        return bool(set(aid_types) & set(self.FINANCIAL_AIDS))

    def is_technical(self):
        """Does this aid have technical parts?"""
        aid_types = self.aid_types or []
        return bool(set(aid_types) & set(self.TECHNICAL_AIDS))

    def has_approaching_deadline(self):
        if not self.submission_deadline:
            return False

        delta = self.submission_deadline - timezone.now().date()
        return delta.days <= settings.APPROACHING_DEADLINE_DELTA

    def has_expired(self):
        if not self.submission_deadline:
            return False

        today = timezone.now().date()
        return self.submission_deadline < today
