from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.flatpages.models import FlatPage


class Page(FlatPage):
    """A static page that can be created/customized in admin."""

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
        on_delete=models.PROTECT,
        null=True, blank=True)
