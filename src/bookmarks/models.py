from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class Bookmark(models.Model):
    """A bookmarked search query."""

    owner = models.ForeignKey(
        'accounts.User',
        verbose_name=_('Owner'),
        on_delete=models.CASCADE)
    querystring = models.TextField(
        _('Querystring'))
    title = models.CharField(
        _('Title'),
        max_length=250)
    send_email_alert = models.BooleanField(
        _('Send email alert'),
        default=False)
    latest_alert_date = models.DateTimeField(
        _('Latest alert date'),
        null=True)
    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)
    date_updated = models.DateTimeField(
        _('Date updated'),
        auto_now=True)

    class Meta:
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmarks')
