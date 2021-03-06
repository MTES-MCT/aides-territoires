from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.sites.models import Site
from django.db.models import Count, Func, F, Value, CharField, Prefetch
from django.db.models.functions import TruncWeek
from django.utils import timezone

from minisites.mixins import NarrowedFiltersMixin
from search.models import SearchPage
from backers.models import Backer
from aids.models import Aid
from aids.views import SearchView, AdvancedSearchView, AidDetailView
from backers.views import BackerDetailView
from programs.views import ProgramDetail
from alerts.views import AlertCreate
from stats.models import AidViewEvent, AidSearchEvent
from stats.utils import log_aidsearchevent
from core.utils import get_site_from_host


class MinisiteMixin:
    """Common code for all minisite urls.

    For every minisite view, we need to fetch the actual SearchPage object and
    inject it into the template.

    Note: there are several ways access the search page, hence there are
    several ways to access the SearchPage slug.

     1/ https://aides-territoires.beta.gouv.fr/recherche/<partner>/
     2/ https://<partner>.aides-territoires.beta.gouv.fr/
     3/ https://aides.<partner>.com (completely custom domain)

    In the fist case, we get the SearchPage's slug from the url parameter;
    Second case, from the subdomain;
    Third case, it is passed by a custom http header set in Nginx's settings.
    """

    def get(self, request, *args, **kwargs):
        self.search_page = self.get_search_page()

        if self.search_page is None:
            # Here, we have a bit of a problem.
            # If the SearchPage object is not found, we can't display a 404
            # error, because the 404 template needs a SearchPage to be
            # displayed.
            # Hence, the best way is to redirect to a sensible url.
            # Those errors are mainly caused by very old links with invalid
            # urls existing in the wild,
            # e.g https://www.aides-territoires.beta.gouv.fr
            return HttpResponseRedirect(self.get_redirection_url())

        return super().get(request, *args, **kwargs)

    def get_redirection_url(self):
        """What url to redirect to in case of missing SearchPage object.

        For now, just redirect to the main site's homepage.
        """
        site = Site.objects.get_current()
        url = 'https://{domain}'.format(domain=site.domain)
        return url

    def get_search_page(self):
        """Get the custom page from url."""

        HEADER = 'X-Minisite-Name'

        if 'search_slug' in self.kwargs:
            page_slug = self.kwargs.get('search_slug')
        elif HEADER in self.request.headers:
            page_slug = self.request.headers[HEADER]
        else:
            host = self.request.get_host()
            page_slug = get_site_from_host(host)

        qs = SearchPage.objects.filter(slug=page_slug)
        try:
            obj = qs.get()
        except qs.model.DoesNotExist:
            obj = None
        return obj

    def get_context_data(self, **kwargs):

        # Canonical url definition
        # E.g we want to mark `aides.francemobilites.fr` as a duplicate of
        # `francemobilites.aides-territoires.beta.gouv.fr`.
        main_site_domain = Site.objects.get_current().domain
        page_subdomain = self.search_page.slug
        canonical_url = 'https://{page_subdomain}.{main_site_domain}'.format(
            page_subdomain=page_subdomain,
            main_site_domain=main_site_domain)

        context = super().get_context_data(**kwargs)
        context['search_page'] = self.search_page
        context['site_url'] = self.request.build_absolute_uri('').rstrip('/')
        context['canonical_url'] = canonical_url

        return context


class SiteHome(MinisiteMixin, NarrowedFiltersMixin, SearchView):
    """A static search page with admin-customizable content."""

    template_name = 'minisites/search_page.html'

    def get_form_kwargs(self):
        """Set the data passed to the form.

        If the form was submitted, the GET values are set, we use those
        instead.
        """
        data = self.request.GET.copy()
        data.pop('page', None)
        data.pop('integration', None)
        kwargs = super().get_form_kwargs()
        kwargs['data'] = data
        return kwargs

    def get_queryset(self):
        """Filter the queryset on the categories and audiences filters."""

        financers_qs = Backer.objects \
            .order_by('aidfinancer__order', 'name')

        instructors_qs = Backer.objects \
            .order_by('aidinstructor__order', 'name')

        # Start from the base queryset and add-up more filtering
        qs = self.search_page.get_base_queryset() \
            .select_related('perimeter', 'author') \
            .prefetch_related(Prefetch('financers', queryset=financers_qs)) \
            .prefetch_related(Prefetch('instructors',
                                       queryset=instructors_qs)) \


        # Combine from filtering with the base queryset
        qs = self.form.filter_queryset(qs, apply_generic_aid_filter=True)

        data = self.form.cleaned_data

        categories = data.get('categories', [])
        if categories:
            qs = qs.filter(categories__in=categories)

        targeted_audiences = data.get('targeted_audiences', [])
        if targeted_audiences:
            qs = qs.filter(targeted_audiences__overlap=targeted_audiences)

        qs = self.form.order_queryset(qs).distinct()

        host = self.request.get_host()
        log_aidsearchevent.delay(
            querystring=self.request.GET.urlencode(),
            results_count=qs.count(),
            source=host)

        return qs


class SiteSearch(MinisiteMixin, AdvancedSearchView):
    """The full search form."""

    template_name = 'minisites/advanced_search.html'


class SiteAid(MinisiteMixin, AidDetailView):
    """The detail page of a single aid."""

    template_name = 'minisites/aid_detail.html'


class SiteAlert(MinisiteMixin, AlertCreate):
    pass


class SiteStats(MinisiteMixin, TemplateView):
    template_name = 'minisites/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # aid count
        context['nb_live_aids'] = self.search_page.get_base_queryset().count()

        beginning_of_2021 = timezone.make_aware(datetime(2021, 1, 1))
        thirty_days_ago = timezone.now() - timedelta(days=30)
        seven_days_ago = timezone.now() - timedelta(days=7)

        # page view count: last 30 days & last 7 days
        search_events = AidSearchEvent.objects \
            .filter(source=self.search_page.slug)

        context['search_count_total'] = search_events.count()
        context['search_count_last_30_days'] = search_events \
            .filter(date_created__gte=thirty_days_ago) \
            .count()
        context['search_count_last_7_days'] = search_events \
            .filter(date_created__gte=seven_days_ago) \
            .count()

        # aid view count: last 30 days & last 7 days
        view_events = AidViewEvent.objects \
            .filter(source=self.search_page.slug)

        context['aid_view_count_last_30_days'] = view_events \
            .filter(date_created__gte=thirty_days_ago) \
            .count()
        context['aid_view_count_last_7_days'] = view_events \
            .filter(date_created__gte=seven_days_ago) \
            .count()

        # aid view grouped by week (since 1/1/2021)
        aid_view_timeseries = view_events \
            .filter(date_created__gte=beginning_of_2021) \
            .annotate(date_to_week=TruncWeek('date_created')) \
            .annotate(day=Func(
                F('date_to_week'),
                Value('YYYY-MM-DD'),
                function='to_char',
                output_field=CharField())) \
            .values('day') \
            .annotate(y=Count('id')) \
            .order_by('day')
        context['aid_view_timeseries'] = list(aid_view_timeseries)

        # top 10 aid viewed
        top_aid_viewed = view_events \
            .select_related('aid') \
            .values('aid_id', 'aid__slug', 'aid__name') \
            .annotate(view_count=Count('aid_id')) \
            .order_by('-view_count')
        context['top_10_aid_viewed'] = list(top_aid_viewed)[:10]

        # top 10 targeted_audiences filters
        if self.search_page.show_audience_field:
            top_audiences_searched = search_events \
                .filter(targeted_audiences__isnull=False) \
                .annotate(audience=Func(
                    F('targeted_audiences'), function='unnest')) \
                .values('audience') \
                .annotate(search_count=Count('id')) \
                .order_by('-search_count')
            # get the display_name of each audience
            for (index, item) in enumerate(top_audiences_searched):
                top_audiences_searched[index]['audience'] = Aid.AUDIENCES[item['audience']]  # noqa
            context['top_10_audiences_searched'] = list(top_audiences_searched)[:10]  # noqa

        # top 10 categories filters
        if self.search_page.show_categories_field:
            top_categories_searched = search_events \
                .prefetch_related('categories') \
                .exclude(categories=None) \
                .values('categories__id', 'categories__name') \
                .annotate(search_count=Count('categories__id')) \
                .order_by('-search_count')
            context['top_10_categories_searched'] = list(top_categories_searched)[:10]  # noqa

        # top 10 keywords searched
        top_keywords_searched = search_events \
            .exclude(text__isnull=True).exclude(text__exact='') \
            .values('text') \
            .annotate(search_count=Count('id')) \
            .order_by('-search_count')
        context['top_10_keywords_searched'] = list(top_keywords_searched)[:10]

        return context


class SiteProgram(MinisiteMixin, ProgramDetail):
    """The detail page of a single program."""

    template_name = 'minisites/program_detail.html'


class SiteBackers(MinisiteMixin, BackerDetailView):
    """The detail page of a single backer."""

    template_name = 'minisites/backer_detail.html'


class SiteLegalMentions(MinisiteMixin, TemplateView):
    template_name = 'minisites/legal_mentions.html'


class Error(MinisiteMixin, TemplateView):
    template_name = 'minisites/404.html'
    status_code = 404

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = self.status_code
        return super().render_to_response(context, **response_kwargs)
