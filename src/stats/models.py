from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from django.contrib.postgres.fields import ArrayField

from core.fields import ChoiceArrayField
from aids.models import Aid


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


class AidSearchEvent(models.Model):
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
    themes = models.ManyToManyField(
        'categories.Theme',
        verbose_name=_('Themes'),
        related_name='aid_search_events',
        blank=True)
    categories = models.ManyToManyField(
        'categories.Category',
        verbose_name=_('Categories'),
        related_name='aid_search_events',
        blank=True)
    text = models.CharField(
        _('Text search'),
        max_length=256,
        null=True, blank=True)

    querystring = models.TextField(
        _('Querystring'))
    results_count = models.PositiveIntegerField(
        _('Results count'),
        default=0)
    source = models.CharField(
        'Source',
        max_length=256,
        default='')

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Aid Search Event')
        verbose_name_plural = _('Aid Search Events')


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
