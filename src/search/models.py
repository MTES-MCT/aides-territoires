from os.path import splitext

from django.db import models
from django.db.models import Count
from django.http import QueryDict
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.fields import ChoiceArrayField
from aids.models import Aid
from aids.constants import AUDIENCES_GROUPED


def logo_upload_to(instance, filename):
    """Rename uploaded files with the object's slug."""

    _, extension = splitext(filename)
    name = instance.slug
    filename = 'minisites/{}_logo{}'.format(
        name, extension)
    return filename


def meta_upload_to(instance, filename):
    """Rename uploaded files with the object's slug."""

    _, extension = splitext(filename)
    name = instance.slug
    filename = 'minisites/{}_meta{}'.format(
        name, extension)
    return filename


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
    short_title = models.CharField(
        _('Short title'),
        max_length=180,
        blank=True, default='',
        help_text=_('A shorter, more concise title.'))
    slug = models.SlugField(
        _('Slug'),
        help_text=_('This part is used in the url. '
                    'DON\'t change this for existing pages. '
                    'MUST be lowercase for minisites.'))
    content = models.TextField(
        _('Page content'),
        help_text=_('Full description of the page. '
                    'Will be displayed above results.'))
    more_content = models.TextField(
        _('Additional page content'),
        blank=True,
        help_text=_('Hidden content, revealed with a `See more` button'))
    search_querystring = models.TextField(
        _('Querystring'),
        help_text=_('The search paramaters url'))
    excluded_aids = models.ManyToManyField(
        'aids.Aid',
        verbose_name=_('Excluded aids'),
        related_name='excluded_from_search_pages',
        blank=True)

    # SEO
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
    meta_image = models.FileField(
        _('Meta image'),
        null=True, blank=True,
        upload_to=meta_upload_to,
        help_text=_('Make sure the file is at least 1024px long.'))

    # custom_colors
    color_1 = models.CharField(
        _('Color 1'),
        max_length=10,
        blank=True,
        help_text=_('Main background color'))
    color_2 = models.CharField(
        _('Color 2'),
        max_length=10,
        blank=True,
        help_text=_('Search form background color'))
    color_3 = models.CharField(
        _('Color 3'),
        max_length=10,
        blank=True,
        help_text=_('Buttons and title borders color'))
    color_4 = models.CharField(
        _('Color 4'),
        max_length=10,
        blank=True,
        help_text=_('Link colors'))
    color_5 = models.CharField(
        _('Color 5'),
        max_length=10,
        blank=True,
        help_text=_('Footer background color'))
    logo = models.FileField(
        _('Logo image'),
        null=True, blank=True,
        upload_to=logo_upload_to,
        help_text=_('Make sure the file is not too heavy. Prefer svg files.'))
    logo_link = models.URLField(
        _('Logo link'),
        null=True, blank=True,
        help_text=_('The url for the partner\'s logo link'))

    # Search form customization fields
    show_categories_field = models.BooleanField(
        _('Show categories field?'),
        default=True)
    available_categories = models.ManyToManyField(
        'categories.Category',
        verbose_name=_('Categories'),
        related_name='search_pages',
        blank=True)

    show_audience_field = models.BooleanField(
        _('Show audience field?'),
        default=True)
    available_audiences = ChoiceArrayField(
        verbose_name=_('Targeted audiences'),
        null=True, blank=True,
        base_field=models.CharField(
            max_length=32,
            choices=AUDIENCES_GROUPED))

    show_perimeter_field = models.BooleanField(
        _('Show perimeter field?'),
        default=True)
    show_mobilization_step_field = models.BooleanField(
        _('Show mobilization step filter?'),
        default=False)
    show_aid_type_field = models.BooleanField(
        _('Show aid type filter?'),
        default=False)

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)
    date_updated = models.DateTimeField(
        _('Date updated'),
        auto_now=True)

    class Meta:
        verbose_name = _('Search page')
        verbose_name_plural = _('Search pages')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('search_page', args=[self.slug])

    def get_base_queryset(self, all_aids=False):
        """Return the list of aids based on the initial search querysting."""

        from aids.forms import AidSearchForm

        # Sometime, the admin person enters a prefix "?" character
        # and we don't want it here.
        querystring = self.search_querystring.strip('?')
        data = QueryDict(querystring)
        form = AidSearchForm(data)
        if all_aids:
            qs = form.filter_queryset(
                qs=Aid.objects.all(),
                apply_generic_aid_filter=False).distinct()
        else:
            qs = form.filter_queryset(
                apply_generic_aid_filter=False).distinct()

        # Also exlude aids contained in the excluded_aids field
        qs = qs.exclude(id__in=self.excluded_aids.values_list('id', flat=True))

        return qs

    def get_aids_per_status(self):
        all_aids_per_status = self.get_base_queryset(all_aids=True) \
                                  .values('status') \
                                  .annotate(count=Count('id', distinct=True))
        return {s['status']: s['count'] for s in list(all_aids_per_status)}
