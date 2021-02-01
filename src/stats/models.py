from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from django.contrib.postgres.fields import ArrayField

from core.fields import ChoiceArrayField
from aids.models import Aid
from search.utils import (
    clean_search_querystring, get_querystring_value_list_from_key,
    get_querystring_perimeter, get_querystring_themes,
    get_querystring_categories)


class AidSearchEvent(models.Model):
    """
    - source : main or PP or api
    - targeted_audiences // choices
    - perimeter // Perimeter
    - themes // Theme
    - categories // Category
    - other: text, programs, apply_before, order_by, call_for_projects_only, integration ?, search ?, action ?, page ?  # noqa
    - Full url
    - Nombre de résultats
    - Timestamp

    --> populate fields asynchronously to avoid slowing down search
    --> add tests
    --> ignore internal api calls (admin, frontend)
    """

    targeted_audiences = ChoiceArrayField(
        verbose_name=_('Targeted audiences'),
        null=True, blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=Aid.AUDIENCES))
    perimeter = models.ForeignKey(
        'geofr.Perimeter',
        verbose_name=_('Perimeter'),
        on_delete=models.PROTECT,
        null=True, blank=True)
    # perimeter = models.CharField(
    #     max_length=150,
    #     verbose_name=_('Perimeter'),
    #     null=True, blank=True)
    themes = models.ManyToManyField(
        'categories.Theme',
        verbose_name=_('Themes'),
        related_name='aid_search_events',
        blank=True)
    # themes = ArrayField(
    #     base_field=models.CharField(max_length=70, blank=True),
    #     verbose_name=_('Themes'),
    #     null=True, blank=True)
    categories = models.ManyToManyField(
        'categories.Category',
        verbose_name=_('Categories'),
        related_name='aid_search_events',
        blank=True)
    # categories = ArrayField(
    #     base_field=models.CharField(max_length=70, blank=True),
    #     verbose_name=_('Categories'),
    #     null=True, blank=True)

    querystring = models.TextField(
        _('Querystring'))

    results_count = models.PositiveIntegerField(
        _('Results count'),
        default=0)

    source = models.CharField(
        'Source',
        max_length=256,
        default='')

    fields_populated = models.BooleanField(
        _('Fields populated?'),
        default=False)

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Aid Search Event')
        verbose_name_plural = _('Aid Search Events')

    def clean_and_populate_search_fields(self):
        """
        Method to cleanup/populate our events
        Run asynchronously to avoid slowing down requests.
        """
        # Filter out empty search values
        if self.querystring:
            self.querystring = clean_search_querystring(self.querystring)
        # Cleanup source field
        # aides-territoires.beta.gouv.fr --> aides-territoires
        # francemobilities.aides-territoires.beta.gouv.fr --> francemobilities
        # aides.francemobilities.fr --> aides.francemobilities.fr
        if self.source:
            if 'aides-territoires' in self.source:
                self.source = self.source.split('.')[0]
        # Populate search fields for futur querying
        if not self.fields_populated:
            if self.querystring:
                self.targeted_audiences = get_querystring_value_list_from_key(self.querystring, 'targeted_audiences') or None  # noqa
                self.perimeter = get_querystring_perimeter(self.querystring)
                self.themes.set(get_querystring_themes(self.querystring))
                self.categories.set(get_querystring_categories(self.querystring))  # noqa
        # Update fields_populated field to avoid re-running this method
        self.fields_populated = True
        self.save()


class AidViewEvent(models.Model):
    aid = models.ForeignKey(
        'aids.Aid',
        verbose_name=_('Aid'),
        on_delete=models.PROTECT)

    querystring = models.TextField(
        _('Querystring'))
    source = models.CharField(
        'Source',
        max_length=256,
        default='')

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Aid View Event')
        verbose_name_plural = _('Aid View Events')


class Event(models.Model):
    """Stores an event in db for analytics purpose."""

    # Category and event describe an event we want to track
    # e.g "alert -> sent" or "aid -> viewed".
    category = models.CharField(
        _('Category'),
        max_length=128)
    event = models.CharField(
        _('Event'),
        max_length=128)

    # Add additional info to describe the event
    # E.g add the slug of the viewed aid.
    meta = models.CharField(
        _('Name'),
        max_length=256,
        default='')
    source = models.CharField(
        'Source',
        max_length=256,
        default='')

    # A numeric value to quantify the event
    # e.g 15 alerts were sent.
    value = models.IntegerField(
        _('Value'))

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        indexes = [
            models.Index(fields=['category', 'event']),
        ]
