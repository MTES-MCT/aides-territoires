from uuid import uuid4

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

from model_utils import Choices
from django_xworkflows import models as xwf_models

from core.fields import ChoiceArrayField


class AidQuerySet(models.QuerySet):
    """Custom queryset with additional filtering methods for aids."""

    def published(self):
        """Only returns published objects."""

        return self.filter(status='published')

    def under_review(self):
        """Return aids that need to be review before publication."""

        return self.filter(status='reviewable')

    def open(self):
        """Returns aids that may appear in the search results (unexpired)."""

        today = timezone.now().date()
        return self.filter(Q(submission_deadline__gte=today) |
                           Q(submission_deadline__isnull=True))


class BaseAidManager(models.Manager):
    """Custom manager to exclude deleted aids from all queries."""

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(status='deleted')
        return qs


ExistingAidsManager = BaseAidManager.from_queryset(AidQuerySet)


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


class Aid(xwf_models.WorkflowEnabled, models.Model):
    """Represents a single Aid."""

    TYPES = Choices(
        ('grant', _('Grant')),
        ('loan', _('Loan')),
        ('recoverable_advance', _('Recoverable advance')),
        ('interest_subsidy', _('Interest subsidy')),
        ('guidance', _('Guidance')),
        ('networking', _('Networking')),
        ('valorisation', _('Valorisation')),
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
        ('department', _('Department')),
        ('region', _('Region')),
        ('epci', _('Audiance EPCI')),
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

    objects = ExistingAidsManager()
    all_aids = AidQuerySet.as_manager()

    slug = models.SlugField(
        _('Slug'),
        help_text=_('Let it empty so it will be autopopulated.'),
        blank=True)
    name = models.CharField(
        _('Name'),
        max_length=256,
        null=False, blank=False)
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        help_text=_('Who is submitting the aid?'))
    backers = models.ManyToManyField(
        'backers.Backer',
        related_name='aids',
        verbose_name=_('Backers'),
        help_text=_('On a national level if appropriate'))
    description = models.TextField(
        _('Short description'),
        max_length=500,
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
        base_field=models.CharField(
            max_length=32,
            choices=STEPS,
            default=STEPS.preop))
    url = models.URLField(
        _('URL'),
        blank=True)
    application_url = models.URLField(
        _('Application url'),
        blank=True)
    targeted_audiances = ChoiceArrayField(
        verbose_name=_('Targeted audiances'),
        base_field=models.CharField(
            max_length=32,
            choices=AUDIANCES))
    aid_types = ChoiceArrayField(
        verbose_name=_('Aid types'),
        base_field=models.CharField(
            max_length=32,
            choices=TYPES),
        help_text=_('Specify the help type or types.'))
    destinations = ChoiceArrayField(
        verbose_name=_('Destinations'),
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
    subvention_rate = models.DecimalField(
        _('Subvention rate (in %)'),
        max_digits=6,
        decimal_places=2,
        null=True, blank=True,
        help_text=_('If this is a subvention aid, specify the rate.'))
    contact_email = models.EmailField(
        _('Contact email'),
        blank=True)
    contact_phone = models.CharField(
        _('Contact phone number'),
        max_length=20,
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

    status = xwf_models.StateField(
        AidWorkflow,
        verbose_name=_('Status'))
    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)
    date_updated = models.DateTimeField(
        _('Date updated'),
        auto_now=True)

    class Meta:
        verbose_name = _('Aid')
        verbose_name_plural = _('Aids')

    def save(self, *args, **kwargs):
        """Populate the slug field.

        Lots of aids have duplicate name, so we prefix the slug with random
        characters.
        """
        if not self.id:
            full_title = '{}-{}'.format(str(uuid4())[:4], self.name)
            self.slug = slugify(full_title)[:50]
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('aid_detail_view', args=[self.slug])

    def is_draft(self):
        return self.status == AidWorkflow.states.draft

    def is_under_review(self):
        return self.status == AidWorkflow.states.reviewable

    def is_published(self):
        return self.status == AidWorkflow.states.published

    def is_financial(self):
        """Does this aid have financial parts?"""
        return bool(set(self.aid_types) & set(self.FINANCIAL_AIDS))

    def is_technical(self):
        """Does this aid have technical parts?"""
        return bool(set(self.aid_types) & set(self.TECHNICAL_AIDS))

    def has_appreaching_deadline(self):
        if not self.submission_deadline:
            return False

        delta = self.submission_deadline - timezone.now().date()
        return delta.days <= settings.APPROACHING_DEADLINE_DELTA
