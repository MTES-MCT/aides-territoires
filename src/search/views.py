from django.views.generic import FormView

from search.forms import GeneralSearchForm


class SearchMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['querystring'] = self.request.GET.urlencode()
        return context


class GeneralSearch(SearchMixin, FormView):
    """general search form."""

    template_name = 'search/general_search.html'
    form_class = GeneralSearchForm
