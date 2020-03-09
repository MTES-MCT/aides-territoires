from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    """Stores an event in db for analytics purpose."""

    category = models.CharField(
        _('Category'),
        max_length=128)
    event = models.CharField(
        _('Event'),
        max_length=128)
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
