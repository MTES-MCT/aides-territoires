import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.http import QueryDict
from django.urls import reverse
from model_utils import Choices

from aids.models import Aid
from search.utils import clean_search_querystring


class Alert(models.Model):
    """A single alert saved by a user."""

    FREQUENCIES = Choices(("daily", "Quotidiennement"), ("weekly", "Hebdomadairement"))

    token = models.UUIDField(
        _("Secret token"), primary_key=True, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(_("Email"))
    querystring = models.TextField(_("Querystring"))
    title = models.CharField(_("Title"), max_length=250)
    alert_frequency = models.CharField(
        max_length=32, choices=FREQUENCIES, default=FREQUENCIES.daily
    )
    source = models.CharField("Source", max_length=256, blank=True, default="")
    validated = models.BooleanField(_("Confirmed?"), default=False)
    date_validated = models.DateTimeField(_("Date validated"), null=True)
    latest_alert_date = models.DateTimeField(
        _("Latest alert date"), default=timezone.now
    )
    date_created = models.DateTimeField(_("Date created"), default=timezone.now)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True)

    class Meta:
        verbose_name = _("Alert")
        verbose_name_plural = _("Alerts")
        ordering = ["-date_created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.clean_querystring()
        return super().save(*args, **kwargs)

    def clean_querystring(self):
        self.querystring = clean_search_querystring(self.querystring)

    def validate(self):
        self.validated = True
        self.date_validated = timezone.now()

    def get_absolute_url(self, in_minisite=False):
        # When accessing the alert URL, we want to keep only
        # things that were published after the last alert was sent.
        querydict = QueryDict(self.querystring).copy()
        published_after = self.latest_alert_date.strftime("%Y-%m-%d")
        querydict["published_after"] = published_after
        querydict["action"] = "alert"
        absolute_url = "{}?{}".format(
            reverse("search_view"), querydict.urlencode()
        )  # noqa
        if in_minisite:
            return absolute_url.replace("/aides/", "/")
        return absolute_url

    def get_new_aids(self):
        """Get the list of aids that match the stored search params."""

        from aids.forms import AidSearchForm

        querydict = QueryDict(self.querystring)
        search_form = AidSearchForm(querydict)
        base_qs = (
            Aid.objects.published()
            .open()
            .select_related("perimeter", "author")
            .prefetch_related("financers")
            .filter(date_published__gte=self.latest_alert_date)
            .order_by("date_published")
        )
        qs = search_form.filter_queryset(base_qs).distinct()
        return qs
