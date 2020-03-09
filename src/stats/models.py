from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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
