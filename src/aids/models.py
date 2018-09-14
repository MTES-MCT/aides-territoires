from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from model_utils import Choices

from core.fields import ChoiceArrayField
from geofr.fields import RegionField, DepartmentField


class AidQuerySet(models.QuerySet):
    """Custom queryset with additional filtering methods for aids."""

    def published(self):
        """Only returns published objects."""

        return self.filter(status='published')

    def open(self):
        """Returns aids that may appear in the search results (unexpired)."""

        today = timezone.now().date()
        return self.filter(Q(submission_deadline__gte=today) |
                           Q(submission_deadline__isnull=True))


class Aid(models.Model):
    """Represents a single Aid."""

    TYPES = Choices(
        ('grant', _('Grant')),
        ('convention', _('Convention')),
        ('training', _('Training')),
        ('interest_subsidy', _('Interest subsidy')),
        ('loan', _('Loan')),
        ('recoverable_advance', _('Recoverable advance')),
        ('guarantee', _('Guarantee')),
        ('low_interest_rate_loan', _('Low interest rate loan')),
        ('capital investment', _('Capital investment')),
        ('tax_benefit', _('Tax benefit')),
        ('return_fund', _('Return fund')),
        ('engineering', _('Engineering')),
        ('guidance', _('Guidance')),
        ('valorisation', _('Valorisation')),
        ('communication', _('Communication')),
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

    STATUSES = Choices(
        ('draft', _('Draft')),
        ('reviewable', _('Review required')),
        ('published', _('Published')),
    )

    AUDIANCES = Choices(
        ('commune', _('Commune')),
        ('department', _('Department')),
        ('region', _('Region')),
        ('epci', _('EPCI')),
    )

    DESTINATIONS = Choices(
        ('service', _('Service (AMO, survey)')),
        ('works', _('Works')),
        ('supply', _('Supply')),
    )

    AID_STATUSES = Choices(
        ('open', _('Open')),
        ('planned', _('Planned')),
        ('closed', _('closed')),
        ('unknown', _('Unknown')),
    )

    RECURRENCE = Choices(
        ('oneoff', _('One off')),
        ('ongoing', _('Ongoing')),
        ('recurring', _('Recurring')),
    )

    objects = AidQuerySet.as_manager()

    name = models.CharField(
        _('Name'),
        max_length=256,
        null=False, blank=False)
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        help_text=_('Who is submitting the aid?'))
    backer = models.ForeignKey(
        'backers.Backer',
        on_delete=models.PROTECT,
        verbose_name=_('Backer'),
        help_text=_('On a national level if appropriate'))
    description = models.TextField(
        _('Short description'),
        max_length=500,
        blank=False)
    eligibility = models.TextField(
        _('Eligibility'),
        blank=False)
    perimeter = models.ForeignKey(
        'geofr.Perimeter',
        verbose_name=_('Perimeter'),
        on_delete=models.PROTECT,
        null=True, blank=True,
        help_text=_('What is the aid broadcasting perimeter?'))
    application_perimeter = models.CharField(
        _('Application perimeter'),
        max_length=32,
        choices=PERIMETERS)
    application_region = RegionField(
        _('Application region'),
        null=True, blank=True)
    application_department = DepartmentField(
        _('Application department'),
        null=True, blank=True)
    mobilization_steps = ChoiceArrayField(
        verbose_name=_('Mobilization step'),
        base_field=models.CharField(
            max_length=32,
            choices=STEPS,
            default=STEPS.preop))
    url = models.URLField(
        _('URL'),
        blank=True)
    targeted_audiances = ChoiceArrayField(
        verbose_name=_('Targeted audiances'),
        base_field=models.CharField(
            max_length=32,
            choices=AUDIANCES))
    is_funding = models.BooleanField(
        _('Is this a funding aid?'),
        default=True)
    aid_types = ChoiceArrayField(
        verbose_name=_('Aid types'),
        base_field=models.CharField(
            max_length=32,
            choices=TYPES),
        help_text=_('Specify the help type or types.'))
    destinations = ChoiceArrayField(
        verbose_name=_('Destinations'),
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
        _('Subvention rate'),
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
    publication_status = models.CharField(
        _('Status'),
        max_length=23,
        choices=AID_STATUSES,
        default=AID_STATUSES.open)
    open_to_third_party = models.BooleanField(
        _('Open to third party?'),
        default=True)
    recurrence = models.CharField(
        _('Recurrence'),
        help_text=_('Is this a one-off aid, is it recurring or ongoing?'),
        max_length=16,
        choices=RECURRENCE,
        blank=True)

    status = models.CharField(
        _('Status'),
        max_length=23,
        choices=STATUSES,
        default=STATUSES.draft)
    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Aid')
        verbose_name_plural = _('Aids')

    def __str__(self):
        return self.name

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
