from datetime import datetime, timedelta
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import Count, Func, F, Value, CharField
from django.db.models.functions import TruncWeek
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, DetailView
from django.views.generic.base import RedirectView

from minisites.mixins import NarrowedFiltersMixin
from search.models import SearchPage
from aids.models import Aid
from aids.views import SearchView, AidDetailView
from backers.views import BackerDetailView
from programs.views import ProgramDetail
from categories.models import Category

from alerts.views import AlertCreate
from search.utils import clean_search_querystring
from stats.models import AidViewEvent, AidSearchEvent
from pages.models import Page
from stats.utils import log_aidsearchevent
from core.utils import get_site_from_host, get_base_url
from aids.forms import AidSearchForm


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
            return HttpResponseRedirect(self.get_ghost_redirection_url())

        if settings.ENABLE_MINISITES_REDIRECTION and self.search_page.subdomain_enabled:
            canonical_url = self.get_canonical_url(subdomain=self.search_page.slug)
            redirect_url = self.get_redirection_url(canonical_url)
            if redirect_url:
                return redirect(redirect_url)
        elif (
            not self.search_page.subdomain_enabled
            and self.request.get_host() != Site.objects.get_current().domain
        ):
            # In case someone tries to access from a previously used subdomain
            # that has been deactivated
            slug = self.search_page.slug
            url = f"{get_base_url()}/portails/{slug}/"

            return HttpResponseRedirect(url)

        return super().get(request, *args, **kwargs)

    def get_search_page(self):
        """Get the custom page from url."""

        if "search_slug" in self.kwargs:
            page_slug = self.kwargs.get("search_slug")
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
        canonical_url = self.get_canonical_url(subdomain=self.search_page.slug)
        context = super().get_context_data(**kwargs)
        context["search_page"] = self.search_page
        if self.search_page.subdomain_enabled is True:
            context["search_page_with_subdomain"] = True
        context["site_url"] = self.request.build_absolute_uri("").rstrip("/")
        context["canonical_url"] = canonical_url

        return context

    def get_canonical_url(self, subdomain):
        """
        Canonical url can be formed with an external DNS for instance:
        `aides.francemobilites.fr`.
        It can also be based on the subdomain, for instance:
        `https://renovation-energetique.aides-territoires.beta.gouv.fr/`.
        """
        for minisite_slug, external_url in settings.REDIRECT_MINISITES_TO_EXTERNAL_URL:
            if minisite_slug == subdomain:
                return external_url
        main_site_domain = Site.objects.get_current().domain
        canonical_url = f"https://{subdomain}.{main_site_domain}"
        return canonical_url

    def get_redirection_url(self, canonical_url):
        """
        Return the target redirection URL.
        When the site host is the same as the canonical URL, we consider that
        we are already using the target URL - no need to redirect anymore.
        """
        if not self.search_page:
            return None
        host_from_request = self.request.get_host()
        host_from_canonical_url = urlparse(canonical_url).netloc
        if host_from_request == host_from_canonical_url:
            return None
        return canonical_url

    def get_ghost_redirection_url(self):
        """What url to redirect to in case of missing SearchPage object.

        For now, just redirect to the main site's homepage.
        """
        url = get_base_url()
        return url


class SiteHome(MinisiteMixin, NarrowedFiltersMixin, SearchView):
    """A static search page with admin-customizable content."""

    template_name = "minisites/search_page.html"

    def get_form_kwargs(self):
        """Set the data passed to the form.

        If the form was submitted, the GET values are set, we use those
        instead.
        """
        data = self.request.GET.copy()
        data.pop("page", None)
        data.pop("integration", None)
        kwargs = super().get_form_kwargs()
        kwargs["data"] = data
        return kwargs

    def get_queryset(self):
        """Filter the queryset with search_page's base_querystring
        and filters choosen by the user."""

        """
        If user does not choose filters,
        we apply only filters from the search_page base_querystring
        These filters are displayed in the front form (with get_context_data)
        and in the filters tags in front.

        Elif user choose filters, we apply the filters displayed in the front form(*).
        (*) filters modified by the user and
        search_page base_querystring filters not modified by user
        """

        if not self.form.data:
            self.form = AidSearchForm(data=self.search_page.get_base_querystring_data())
            if self.search_page.available_categories:
                if len(self.get_available_categories()) >= 1:
                    available_categories = self.get_available_categories()
                else:
                    available_categories = Category.objects.select_related(
                        "theme"
                    ).order_by("theme__name", "name")
                self.form.fields["categories"].queryset = available_categories
            if self.search_page.available_audiences:
                available_audiences = self.get_available_audiences()
                self.form.fields["targeted_audiences"].choices = available_audiences

        qs = self.form.filter_queryset(
            self.search_page.get_base_queryset(), apply_generic_aid_filter=True
        )

        # if order_by filter exists in the base querystring we want to use it,
        # combine with hightlighted_aids order
        order = self.search_page.get_base_querystring_data().get("order_by")
        qs = self.form.order_queryset(
            qs, has_highlighted_aids=True, pre_order=order
        ).distinct()

        host = self.request.get_host()
        request_ua = self.request.META.get("HTTP_USER_AGENT", "")

        # handle case search_page is not displayed in a subdomain
        if "/portails/" in self.request.path:
            path = self.request.path.partition("/portails/")[2]
            host = path.partition("/")[0]

        log_aidsearchevent.delay(
            querystring=self.request.GET.urlencode(),
            results_count=qs.count(),
            source=host,
            request_ua=request_ua,
        )

        return qs

    def get_context_data(self, **kwargs):
        pages = Page.objects.filter(minisite=self.search_page)

        # We need to add form to context data to populate all filters* in front form input(s)
        # all filters = filters from the search_page's querystring and filters choosen by user
        form = self.form

        context = super().get_context_data(pages=pages, form=form, **kwargs)

        context["base_search_url"] = get_base_url() + "/aides/"

        context["querystring_cleaned"] = clean_search_querystring(
            self.search_page.search_querystring
        )
        return context


class SiteAid(MinisiteMixin, AidDetailView):
    """The detail page of a single aid."""

    template_name = "minisites/aid_detail.html"


class SiteAlert(MinisiteMixin, AlertCreate):
    pass


class SiteStats(MinisiteMixin, TemplateView):
    template_name = "minisites/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.search_page.id == 2:
            context["france_mobilites"] = True

        # aid count
        context["nb_live_aids"] = self.search_page.get_base_queryset().count()

        beginning_of_2021 = timezone.make_aware(datetime(2021, 6, 1))
        thirty_days_ago = timezone.now() - timedelta(days=30)
        seven_days_ago = timezone.now() - timedelta(days=7)

        # page view count: last 30 days & last 7 days
        search_events = AidSearchEvent.objects.filter(source=self.search_page.slug)

        context["search_count_total"] = search_events.count()
        context["search_count_last_30_days"] = search_events.filter(
            date_created__gte=thirty_days_ago
        ).count()
        context["search_count_last_7_days"] = search_events.filter(
            date_created__gte=seven_days_ago
        ).count()

        # aid view count: last 30 days & last 7 days
        view_events = AidViewEvent.objects.filter(source=self.search_page.slug)

        context["aid_view_count_last_30_days"] = view_events.filter(
            date_created__gte=thirty_days_ago
        ).count()
        context["aid_view_count_last_7_days"] = view_events.filter(
            date_created__gte=seven_days_ago
        ).count()

        # aid view grouped by week (since 1/1/2021)
        aid_view_timeseries = (
            view_events.filter(date_created__gte=beginning_of_2021)
            .annotate(date_to_week=TruncWeek("date_created"))
            .annotate(
                day=Func(
                    F("date_to_week"),
                    Value("YYYY-MM-DD"),
                    function="to_char",
                    output_field=CharField(),
                )
            )
            .values("day")
            .annotate(y=Count("id"))
            .order_by("day")
        )
        context["aid_view_timeseries"] = list(aid_view_timeseries)

        # top 10 aid viewed
        top_aid_viewed = (
            view_events.filter(date_created__gte=beginning_of_2021)
            .select_related("aid")
            .values("aid_id", "aid__slug", "aid__name")
            .annotate(view_count=Count("aid_id"))
            .order_by("-view_count")
        )
        context["top_10_aid_viewed"] = list(top_aid_viewed)[:10]

        # top 10 targeted_audiences filters
        if self.search_page.show_audience_field:
            top_audiences_searched = (
                search_events.filter(targeted_audiences__isnull=False)
                .filter(date_created__gte=beginning_of_2021)
                .annotate(audience=Func(F("targeted_audiences"), function="unnest"))
                .values("audience")
                .annotate(search_count=Count("id"))
                .order_by("-search_count")
            )
            # get the display_name of each audience
            for index, item in enumerate(top_audiences_searched):
                try:
                    top_audiences_searched[index]["audience"] = Aid.AUDIENCES[
                        item["audience"]
                    ]  # noqa
                except KeyError:
                    top_audiences_searched[index]["audience"] = item["audience"]  # noqa
            context["top_10_audiences_searched"] = list(top_audiences_searched)[
                :10
            ]  # noqa

        # top 10 categories filters
        # if self.search_page.show_categories_field:
        #     top_categories_searched = search_events \
        #         .prefetch_related(Prefetch('categories', queryset=Category.objects.all())) \
        #         .exclude(categories=None) \
        #         .values('categories__name') \
        #         .annotate(search_count=Count('categories')) \
        #         .order_by('-search_count')
        #     context['top_10_categories_searched'] = list(top_categories_searched)[:10]  # noqa

        # top 10 keywords searched
        top_keywords_searched = (
            search_events.filter(date_created__gte=beginning_of_2021)
            .exclude(text__isnull=True)
            .exclude(text__exact="")
            .values("text")
            .annotate(search_count=Count("id"))
            .order_by("-search_count")
        )
        context["top_10_keywords_searched"] = list(top_keywords_searched)[:10]

        return context


class SiteProgram(MinisiteMixin, ProgramDetail):
    """The detail page of a single program."""

    template_name = "minisites/program_detail.html"


class SiteBackers(MinisiteMixin, BackerDetailView):
    """The detail page of a single backer."""

    template_name = "minisites/backer_detail.html"


class SiteLegalMentions(MinisiteMixin, TemplateView):
    template_name = "minisites/legal_mentions.html"


class SiteTerms(MinisiteMixin, TemplateView):
    template_name = "minisites/cgu.html"


class SitePrivacyPolicy(MinisiteMixin, TemplateView):
    template_name = "minisites/privacy_policy.html"


class SiteAccessibility(MinisiteMixin, TemplateView):
    template_name = "minisites/accessibility.html"


class Error(MinisiteMixin, TemplateView):
    template_name = "minisites/404.html"
    status_code = 404

    def render_to_response(self, context, **response_kwargs):
        response_kwargs["status"] = self.status_code
        return super().render_to_response(context, **response_kwargs)


class PageList(MinisiteMixin, RedirectView):
    pattern_name = "home"


class PageDetail(MinisiteMixin, DetailView):
    template_name = "minisites/page_detail.html"
    context_object_name = "page"

    def get_context_data(self, **kwargs):
        pages = Page.objects.filter(minisite=self.search_page)
        return super().get_context_data(pages=pages, **kwargs)

    def get_object(self):
        url = self.kwargs.get("url")
        if not url.startswith("/"):
            url = "/" + url

        try:
            page = Page.objects.filter(minisite=self.search_page).get(url=url)
        except Page.DoesNotExist:
            raise Http404("No page found")

        return page
