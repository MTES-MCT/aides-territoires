from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.sites.models import Site

from search.models import SearchPage
from geofr.models import Perimeter
from aids.models import Aid
from aids.views import SearchView, AdvancedSearchView, AidDetailView
from alerts.views import AlertCreate


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
            page_slug = host.split('.')[0]

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


class SiteHome(MinisiteMixin, SearchView):
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

    def get_available_categories(self):
        """Return the list of categories available in this minisite.
        Available categories are the one we select in the SearchPage admin
        page.

        When the available categories are defined in the admin, we will
        display them in search form filter.

        There is an initial filtering that applies on the list of aids when
        loading the minisite page. That initial filtering is based on the
        querystring field and is not affected by the selection of available
        categories.
        """
        if not hasattr(self, 'available_categories'):
            page_categories = self.search_page \
                .available_categories \
                .select_related('theme')
            self.available_categories = page_categories
        return self.available_categories

    def get_available_audiences(self):
        """Return the list of audiences available in this minisite."""

        all_audiences = list(Aid.AUDIENCES)
        available_audiences = self.search_page.available_audiences or []
        filtered_audiences = [
            audience for audience in all_audiences
            if audience[0] in available_audiences
        ]
        return filtered_audiences

    def get_available_perimeters(self):
        """Return the list of perimeters available in this minisite.
        Available perimeters are the one we select in the SearchPage admin
        page.

        When the available perimeters are defined in the admin, we will
        display them in search form filter.
        """
        if not hasattr(self, 'available_perimeters'):
            page_perimeters = self.search_page \
                .available_perimeters
            self.available_perimeters = page_perimeters
        return self.available_perimeters
    

    def get_form(self, form_class=None):
        """Returns the aid search and filter form.

        The minisite feature allows admin to filter the available values for
        some filters (audiences and categories).
        """
        form = super().get_form(form_class)

        # Show available values in categories filter field
        available_categories = self.get_available_categories()
        form.fields['categories'].queryset = available_categories

        # Show available values in the targeted audience filter field
        available_audiences = self.get_available_audiences()
        form.fields['targeted_audiences'].choices = available_audiences

        # Show available values in perimeters filter field
        available_perimeters = self.get_available_perimeters()
        form.fields['perimeter'].queryset = available_perimeters

        return form

    def get_queryset(self):
        """Filter the queryset on the categories and audiences filters."""

        # Start from the base queryset and add-up more filtering
        qs = self.search_page.get_base_queryset()

        # Combine from filtering with the base queryset
        qs = self.form.filter_queryset(qs)

        data = self.form.cleaned_data

        categories = data.get('categories', [])
        if categories:
            qs = qs.filter(categories__in=categories)

        targeted_audiences = data.get('targeted_audiences', [])
        if targeted_audiences:
            qs = qs.filter(targeted_audiences__overlap=targeted_audiences)

        perimeter = data.get('perimeter', [])
        if perimeter:
            qs = qs.filter(perimeter_in=perimeter)

        return qs


class SiteSearch(MinisiteMixin, AdvancedSearchView):
    """The full search form."""

    template_name = 'minisites/advanced_search.html'


class SiteAid(MinisiteMixin, AidDetailView):
    """The detail page of a single aid."""

    template_name = 'minisites/aid_detail.html'


class SiteAlert(MinisiteMixin, AlertCreate):
    pass


class SiteLegalMentions(MinisiteMixin, TemplateView):
    template_name = 'minisites/legal_mentions.html'


class Error(MinisiteMixin, TemplateView):
    template_name = 'minisites/404.html'
    status_code = 404

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = self.status_code
        return super().render_to_response(context, **response_kwargs)
