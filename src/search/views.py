from django.views.generic import FormView
from django.http import QueryDict, Http404

from aids.forms import AidSearchForm
from aids.views import SearchView
from search.models import SearchPage
from search.forms import (AudianceSearchForm, PerimeterSearchForm,
                          ThemeSearchForm, CategorySearchForm)


class SearchMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['querystring'] = self.request.GET.urlencode()
        return context


class AudianceSearch(SearchMixin, FormView):
    """Step 1 of the multi-page search form."""

    template_name = 'search/step_audiance.html'
    form_class = AudianceSearchForm


class PerimeterSearch(SearchMixin, FormView):
    """Step 2 of the multi-page search form."""

    template_name = 'search/step_perimeter.html'
    form_class = PerimeterSearchForm

    def get_initial(self):
        GET = self.request.GET
        initial = {
            'targeted_audiances': GET.getlist('targeted_audiances', ''),
        }
        return initial


class ThemeSearch(SearchMixin, FormView):
    """Step 3 of the multi-page search form."""

    template_name = 'search/step_theme.html'
    form_class = ThemeSearchForm

    def get_initial(self):
        GET = self.request.GET
        initial = {
            'targeted_audiances': GET.getlist('targeted_audiances', ''),
            'perimeter': GET.get('perimeter', ''),
        }
        return initial


class CategorySearch(SearchMixin, FormView):
    """Step 4 of the multi-page search form."""

    template_name = 'search/step_category.html'
    form_class = CategorySearchForm

    def get_initial(self):
        GET = self.request.GET
        initial = {
            'targeted_audiances': GET.getlist('targeted_audiances', ''),
            'perimeter': GET.get('perimeter', ''),
            'themes': GET.getlist('themes', []),
        }
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        initial = self.get_initial()
        filter_form = AidSearchForm(initial)
        theme_aids = filter_form.filter_queryset()

        context['total_aids'] = theme_aids \
            .values('id') \
            .distinct() \
            .count()
        return context
