from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from core.fields import ChoiceArrayField
from aids.models import Aid
from geofr.models import Perimeter
from categories.models import Theme, Category


class AidSearchEvent(models.Model):
    """
    - source : main or PP or api
    - targeted_audiences // choices
    - perimeter // Perimeter
    - themes // Theme
    - categories // Category
    - other: text, programs, apply_before, order_by, call_for_projects_only, integration ?, search ?, action ?, page ?
    - Full url
    - Nombre de résultats
    - Timestamp

    --> populate fields asynchronously to avoid slowing down search
    --> add tests
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
        null=True, blank=True,
        help_text=_('What is the searched perimeter?'))
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

    raw_search = models.JSONField(
         _('Raw search query'),
        blank=True)

    results_count = models.PositiveIntegerField(
        _('Results count'))

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

    def set_search_fields(self):
        """Populate instance search fields."""
        if not self.fields_populated:
            if self.raw_search:
                targeted_audiences = self.raw_search.get('targeted_audiences', None)
                if len(targeted_audiences):
                    self.targeted_audiences = targeted_audiences
                perimeter = self.raw_search.get('perimeter', None)
                if len(perimeter):
                    perimeter_id_str = perimeter[0].split('-')[0]
                    self.perimeter = Perimeter.objects.get(id=perimeter_id_str)
                themes = self.raw_search.get('themes', None)
                if len(themes):
                    self.themes.set(Theme.objects.filter(slug__in=themes))
                categories = self.raw_search.get('categories', None)
                if len(categories):
                    self.categories.set(Category.objects.filter(slug__in=categories))
        self.fields_populated = True
        self.save()

    def save(self, *args, **kwargs):
        # self.set_search_fields()
        return super().save(*args, **kwargs)


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
