from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.fields import ChoiceArrayField
from aids.models import Aid


class AidViewEvent(models.Model):
    aid = models.ForeignKey(
        'aids.Aid',
        verbose_name=_('Aid'),
        on_delete=models.PROTECT)

    targeted_audiences = ChoiceArrayField(
        verbose_name=_('Targeted audiences'),
        null=True, blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=Aid.AUDIENCES))

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


class AidContactClickEvent(models.Model):
    aid = models.ForeignKey(
        'aids.Aid',
        verbose_name=_('Aid'),
        on_delete=models.PROTECT)

    querystring = models.TextField(
        _('Querystring'),
        default='')
    source = models.CharField(
        'Source',
        max_length=256,
        blank=True, default='')

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = 'Événement aide voir les contacts'
        verbose_name_plural = 'Événements aide voir les contacts'


class AidOriginUrlClickEvent(models.Model):
    aid = models.ForeignKey(
        'aids.Aid',
        verbose_name=_('Aid'),
        on_delete=models.PROTECT)

    querystring = models.TextField(
        _('Querystring'),
        default='')
    source = models.CharField(
        'Source',
        max_length=256,
        blank=True, default='')

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = 'Événement aide lien vers la démarche en ligne'
        verbose_name_plural = 'Événements aide lien vers la démarche en ligne'


class AidApplicationUrlClickEvent(models.Model):
    aid = models.ForeignKey(
        'aids.Aid',
        verbose_name=_('Aid'),
        on_delete=models.PROTECT)

    querystring = models.TextField(
        _('Querystring'),
        default='')
    source = models.CharField(
        'Source',
        max_length=256,
        blank=True, default='')

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = 'Événement aide candidater'
        verbose_name_plural = 'Événements aide candidater'


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

    backers = models.ManyToManyField(
        'backers.Backer',
        verbose_name=_('Backers'),
        related_name='aid_search_events',
        blank=True)
    programs = models.ManyToManyField(
        'programs.Program',
        verbose_name=_('Programs'),
        related_name='aid_search_events',
        blank=True)
    text = models.CharField(
        _('Text search'),
        max_length=256,
        blank=True, default='')

    querystring = models.TextField(
        _('Querystring'))
    results_count = models.PositiveIntegerField(
        _('Results count'),
        default=0)
    source = models.CharField(
        'Source',
        max_length=256,
        blank=True, default='')

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Aid Search Event')
        verbose_name_plural = _('Aid Search Events')

    def save(self, *args, **kwargs):
        self.clean_fields()
        return super().save(*args, **kwargs)

    def clean_fields(self):
        self.text = self.text[:256] if self.text else ''
        self.source = self.source[:256] if self.source else ''


class AidEligibilityTestEvent(models.Model):
    aid = models.ForeignKey(
        'aids.Aid',
        verbose_name=_('Aid'),
        on_delete=models.PROTECT)
    eligibility_test = models.ForeignKey(
        'eligibility.EligibilityTest',
        verbose_name=_('Eligibility test'),
        on_delete=models.PROTECT)

    answer_success = models.BooleanField(null=True)
    answer_details = models.JSONField(null=True)

    querystring = models.TextField(
        _('Querystring'),
        default='')
    source = models.CharField(
        'Source',
        max_length=256,
        blank=True, default='')

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = 'Événement test d\'éligibilité'
        verbose_name_plural = 'Événements tests d\'éligibilité'


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


class PromotionDisplayEvent(models.Model):
    promotion = models.ForeignKey(
        'blog.PromotionPost',
        verbose_name=_('Promotion Post'),
        on_delete=models.PROTECT)

    querystring = models.TextField(
        _('Querystring'),
        default='')

    source = models.CharField(
        'Source',
        max_length=256,
        blank=True, default='')

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Événement affichage promotion')
        verbose_name_plural = _('Événements affichage promotion')


class PromotionClickEvent(models.Model):
    promotion = models.ForeignKey(
        'blog.PromotionPost',
        verbose_name=_('Promotion Post'),
        on_delete=models.PROTECT)

    querystring = models.TextField(
        _('Querystring'),
        default='')

    source = models.CharField(
        'Source',
        max_length=256,
        blank=True, default='')

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Événement click promotion')
        verbose_name_plural = _('Événements click promotion')
