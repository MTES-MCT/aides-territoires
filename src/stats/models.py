from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    """Stores an event in db for analytics purpose."""

    name = models.CharField(
        _('Name'),
        max_length=128,
        db_index=True)
    value = models.IntegerField(
        _('Value'))
    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
