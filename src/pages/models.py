from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.flatpages.models import FlatPage


class PageQueryset(models.QuerySet):
    def at_pages(self):
        """Pages belonging to Aides-territoires main site."""

        return self.filter(minisite__isnull=True)

    def minisite_pages(self):
        """Pages belonging to minisites."""

        return self.filter(minisite__isnull=False)


class Page(FlatPage):
    """A static page that can be created/customized in admin."""

    objects = PageQueryset.as_manager()

    meta_title = models.CharField(
        _('Meta title'),
        max_length=180,
        blank=True, default='',
        help_text=_('This will be displayed in SERPs. '
                    'Keep it under 60 characters. '
                    'Leave empty and we will reuse the page title.'))
    meta_description = models.TextField(
        _('Meta description'),
        blank=True, default='',
        max_length=256,
        help_text=_('This will be displayed in SERPs. '
                    'Keep it under 120 characters.'))

    minisite = models.ForeignKey(
        'search.SearchPage',
        verbose_name=_('Minisite'),
        help_text=_('Optional, link this page to a minisite.'),
        on_delete=models.PROTECT,
        null=True, blank=True)

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)
    date_updated = models.DateTimeField(
        _('Date updated'),
        auto_now=True)
