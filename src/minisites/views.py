from django.http import QueryDict, Http404

from search.models import SearchPage
from aids.views import SearchView, AdvancedSearchView


class Home(SearchView):
    """A static search page with admin-customizable content."""

    template_name = 'minisites/search_page.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self):
        host = self.request.get_host()
        page_slug = host.split('.')[0]
        qs = SearchPage.objects.filter(slug=page_slug)
        try:
            obj = qs.get()
        except qs.model.DoesNotExist:
            raise Http404('No "Search page" found matching the query')
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = QueryDict(self.object.search_querystring)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_page'] = self.get_object()
        return context


class Search(AdvancedSearchView):
    pass
