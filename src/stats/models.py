from django.db import models
from django.utils import timezone

from core.fields import ChoiceArrayField
from aids.models import Aid


class AccountRegisterFromNextpagewarningClickEvent(models.Model):
    querystring = models.TextField("Querystring", default="")
    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = (
            "Événement compte clic sur le bouton Register-from-Next-Page-Warning"
        )
        verbose_name_plural = (
            "Événements compte clic sur le bouton Register-from-Next-Page-Warning"
        )


class AidViewEvent(models.Model):
    aid = models.ForeignKey("aids.Aid", verbose_name="Aide", on_delete=models.PROTECT)

    targeted_audiences = ChoiceArrayField(
        verbose_name="Bénéficiaires de l’aide",
        null=True,
        blank=True,
        base_field=models.CharField(max_length=32, choices=Aid.AUDIENCES),
    )

    querystring = models.TextField("Querystring")
    source = models.CharField("Source", max_length=256, default="")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Événement aide vue"
        verbose_name_plural = "Événement aides vues"


class AidContactClickEvent(models.Model):
    aid = models.ForeignKey("aids.Aid", verbose_name="Aide", on_delete=models.PROTECT)

    querystring = models.TextField("Querystring", default="")
    source = models.CharField("Source", max_length=256, blank=True, default="")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Événement aide voir les contacts"
        verbose_name_plural = "Événements aide voir les contacts"


class AidOriginUrlClickEvent(models.Model):
    aid = models.ForeignKey("aids.Aid", verbose_name="Aide", on_delete=models.PROTECT)

    querystring = models.TextField("Querystring", default="")
    source = models.CharField("Source", max_length=256, blank=True, default="")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Événement aide lien vers la démarche en ligne"
        verbose_name_plural = "Événements aide lien vers la démarche en ligne"


class AidApplicationUrlClickEvent(models.Model):
    aid = models.ForeignKey("aids.Aid", verbose_name="Aide", on_delete=models.PROTECT)

    querystring = models.TextField("Querystring", default="")
    source = models.CharField("Source", max_length=256, blank=True, default="")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Événement aide candidater"
        verbose_name_plural = "Événements aide candidater"


class AidSearchEvent(models.Model):
    targeted_audiences = ChoiceArrayField(
        verbose_name="Bénéficiaires de l’aide",
        null=True,
        blank=True,
        base_field=models.CharField(max_length=32, choices=Aid.AUDIENCES),
    )
    perimeter = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="Périmètre",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    themes = models.ManyToManyField(
        "categories.Theme",
        verbose_name="Thématiques",
        related_name="aid_search_events",
        blank=True,
    )
    categories = models.ManyToManyField(
        "categories.Category",
        verbose_name="Sous-thématiques",
        related_name="aid_search_events",
        blank=True,
    )

    backers = models.ManyToManyField(
        "backers.Backer",
        verbose_name="Porteurs d’aides",
        related_name="aid_search_events",
        blank=True,
    )
    programs = models.ManyToManyField(
        "programs.Program",
        verbose_name="Programmes",
        related_name="aid_search_events",
        blank=True,
    )
    text = models.CharField(
        "Recherche textuelle", max_length=256, blank=True, default=""
    )

    querystring = models.TextField("Querystring")
    results_count = models.PositiveIntegerField("Nombre de résultats", default=0)
    source = models.CharField("Source", max_length=256, blank=True, default="")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Événement recherche d’aides"
        verbose_name_plural = "Événements recherche d’aides"

    def save(self, *args, **kwargs):
        self.clean_fields()
        return super().save(*args, **kwargs)

    def clean_fields(self):
        self.text = self.text[:256] if self.text else ""
        self.source = self.source[:256] if self.source else ""


class AidEligibilityTestEvent(models.Model):
    aid = models.ForeignKey("aids.Aid", verbose_name="Aide", on_delete=models.PROTECT)
    eligibility_test = models.ForeignKey(
        "eligibility.EligibilityTest",
        verbose_name="Test d’éligibilité",
        on_delete=models.PROTECT,
    )

    answer_success = models.BooleanField(null=True)
    answer_details = models.JSONField(null=True)

    querystring = models.TextField("Querystring", default="")
    source = models.CharField("Source", max_length=256, blank=True, default="")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Événement test d'éligibilité"
        verbose_name_plural = "Événements tests d'éligibilité"


class Event(models.Model):
    """Stores an event in db for analytics purpose."""

    # Category and event describe an event we want to track
    # e.g "alert -> sent" or "aid -> viewed".
    category = models.CharField("Sous-thématique", max_length=128)
    event = models.CharField("Événement", max_length=128)

    # Add additional info to describe the event
    # E.g add the slug of the viewed aid.
    meta = models.CharField("Nom", max_length=256, default="")
    source = models.CharField("Source", max_length=256, default="")

    # A numeric value to quantify the event
    # e.g 15 alerts were sent.
    value = models.IntegerField("Valeur")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        indexes = [
            models.Index(fields=["category", "event"]),
        ]


class PromotionDisplayEvent(models.Model):
    promotion = models.ForeignKey(
        "blog.PromotionPost",
        verbose_name="Communication promotionnelle",
        on_delete=models.PROTECT,
    )

    querystring = models.TextField("Querystring", default="")

    source = models.CharField("Source", max_length=256, blank=True, default="")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Événement affichage promotion"
        verbose_name_plural = "Événements affichage promotion"


class PromotionClickEvent(models.Model):
    promotion = models.ForeignKey(
        "blog.PromotionPost",
        verbose_name="Communication promotionnelle",
        on_delete=models.PROTECT,
    )

    querystring = models.TextField("Querystring", default="")

    source = models.CharField("Source", max_length=256, blank=True, default="")

    date_created = models.DateTimeField("Date de création", default=timezone.now)

    class Meta:
        verbose_name = "Événement click promotion"
        verbose_name_plural = "Événements click promotion"
