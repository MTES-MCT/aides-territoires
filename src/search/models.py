from django.db import models
from django.utils.translation import ugettext_lazy as _


class SearchPage(models.Model):
    """A single search result page with additional data.

    A customized search page is a pre-filtered search page with it's own url,
    configurable titles, descriptions, etc. and built for navigation and
    seo purpose.
    """

    title = models.CharField(
        _('Title'),
        max_length=180,
        help_text=_('The main displayed title.'))
    meta_title = models.CharField(
        _('Meta title'),
        max_length=180,
        blank=True, default='',
        help_text=_('This will be displayed in SERPs. '
                    'Keep it under 60 characters. '
                    'Leave empty and we will reuse the page title.'))
    slug = models.SlugField(
        _('Slug'),
        help_text=_('This part is used in the url. '
                    'DON\'t change this for existing pages.'))

    meta_description = models.TextField(
        _('Meta description'),
        blank=True, default='',
        max_length=256,
        help_text=_('This will be displayed in SERPs. '
                    'Keep it under 120 characters.'))
    content = models.TextField(
        _('Page content'),
        help_text=_('Full description of the page. '
                    'Will be displayed above results.'))
    search_querystring = models.TextField(
        _('Querystring'),
        help_text=_('The search paramaters url'))

    class Meta:
        verbose_name = _('Search page')
        verbose_name_plural = _('Search pages')
