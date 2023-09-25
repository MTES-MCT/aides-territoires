import uuid

from django.db import models
from django.utils import timezone
from django.http import QueryDict
from django.urls import reverse
from model_utils import Choices

from aids.models import Aid
from search.utils import clean_search_querystring
from search.models import SearchPage


class Alert(models.Model):
    """A single alert saved by a user."""

    FREQUENCIES = Choices(("daily", "Quotidiennement"), ("weekly", "Hebdomadairement"))

    token = models.UUIDField(
        "Clé secrète", primary_key=True, default=uuid.uuid4, editable=False
    )
    email = models.EmailField("Courriel")
    querystring = models.TextField("Querystring")
    title = models.CharField("Titre", max_length=250)
    alert_frequency = models.CharField(
        max_length=32, choices=FREQUENCIES, default=FREQUENCIES.daily
    )
    source = models.CharField("Source", max_length=256, blank=True, default="")
    validated = models.BooleanField("Confirmée ?", default=False)
    date_validated = models.DateTimeField("Date de validation", null=True)
    latest_alert_date = models.DateTimeField("Dernière alerte", default=timezone.now)
    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Alerte"
        verbose_name_plural = "Alertes"
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
        absolute_url = "{}?{}".format(reverse("search_view"), querydict.urlencode())
        if in_minisite:
            search_page = SearchPage.objects.filter(slug=self.source).first()
            if search_page and search_page.subdomain_enabled is not True:
                absolute_url = "{}?{}".format(
                    reverse("search_minisite_view", args=[self.source]),
                    querydict.urlencode(),
                )
            else:
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
