from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.http import QueryDict
from django.urls import reverse
from model_utils import Choices

from aids.models import Aid


class Bookmark(models.Model):
    """A bookmarked search query.

    Note: at the beginning, the feature was about saving the current search
    and keeping a list of your saved searches.

    After some time, we added the possibility to receive e-mail alerts
    for saved searches, and it was decided in the UI to put the
    emphasis on the "alert" part.

    Thus, in the code, we handle `bookmarks` but you will see the related
    features as `alerts`.
    """

    FREQUENCIES = Choices(
        ('daily', 'Quotidiennement'),
        ('weekly', 'Hebdomadairement')
    )

    owner = models.ForeignKey(
        'accounts.User',
        verbose_name=_('Owner'),
        related_name='bookmarks',
        on_delete=models.CASCADE)
    querystring = models.TextField(
        _('Querystring'))
    title = models.CharField(
        _('Title'),
        max_length=250)
    send_email_alert = models.BooleanField(
        _('Send email alert'),
        default=False)
    alert_frequency = models.CharField(
        max_length=32,
        choices=FREQUENCIES,
        default=FREQUENCIES.daily)
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
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmarks')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '{}?{}'.format(
            reverse('search_view'),
            self.querystring)

    def get_new_aids(self):
        """Get the list of aids that match the stored search params."""

        from aids.forms import AidSearchForm

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
