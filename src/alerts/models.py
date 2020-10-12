import uuid
import datetime
from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.http import QueryDict
from django.urls import reverse
from model_utils import Choices

from aids.models import Aid
from aids.forms import AidSearchForm


class Alert(models.Model):
    """A single alert saved by a user."""

    FREQUENCIES = Choices(
        ('daily', _('Daily')),
        ('weekly', _('Weekly'))
    )

    token = models.UUIDField(
        _('Secret token'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    email = models.EmailField(
        _('Email'))
    querystring = models.TextField(
        _('Querystring'))
    title = models.CharField(
        _('Title'),
        max_length=250)
    alert_frequency = models.CharField(
        max_length=32,
        choices=FREQUENCIES,
        default=FREQUENCIES.daily)
    validated = models.BooleanField(
        _('Confirmed?'),
        default=False)
    date_validated = models.DateTimeField(
        _('Date validated'),
        null=True)
    latest_alert_date = models.DateTimeField(
        _('Latest alert date'),
        default=timezone.now)
    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)
    date_updated = models.DateTimeField(
        _('Date updated'),
        auto_now=True)

    class Meta:
        verbose_name = _('Alert')
        verbose_name_plural = _('Alerts')
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def validate(self):
        self.validated = True
        self.date_validated = timezone.now()

    def get_absolute_url(self):
        latest_alert_date_str = self.latest_alert_date.date()
        querydict = QueryDict(self.querystring)
        querydict = querydict.copy()
        querydict.setlist('published_after', {latest_alert_date_str}) 
        return '{}?{}'.format(
            reverse('search_view'), 
            querydict.urlencode())

    def get_new_aids(self):
        """Get the list of aids that match the stored search params."""

        querydict = QueryDict(self.querystring)
        search_form = AidSearchForm(querydict)
        base_qs = Aid.objects \
            .published() \
            .open() \
            .select_related('perimeter', 'author') \
            .prefetch_related('financers') \
            .filter(date_published__gte=self.latest_alert_date) \
            .order_by('date_published')
        qs = search_form.filter_queryset(base_qs)
        return qs
