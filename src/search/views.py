from django.views.generic import FormView

from projects.forms import ProjectSuggestForm
from aids.forms import AidSearchForm
from search.forms import (AudienceSearchForm, PerimeterSearchForm,
                          ThemeSearchForm, CategorySearchForm,
                          ProjectSearchForm, AdvancedSearchForm)

from django.shortcuts import redirect, render


class SearchMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['querystring'] = self.request.GET.urlencode()
        context['project_form'] = ProjectSuggestForm(label_suffix='')
        return context


class AudienceSearch(SearchMixin, FormView):
    """Step 1 of the multi-page search form."""

    template_name = 'search/step_audience.html'
    form_class = AudienceSearchForm


class PerimeterSearch(SearchMixin, FormView):
    """Step 2 of the multi-page search form."""

    template_name = 'search/step_perimeter.html'
    form_class = PerimeterSearchForm

    def get_initial(self):
        GET = self.request.GET
        initial = {
            'targeted_audiences': GET.getlist('targeted_audiences', ''),
        }
        return initial


class ThemeSearch(SearchMixin, FormView):
    """Step 3 of the multi-page search form."""

    template_name = 'search/step_theme.html'
    form_class = ThemeSearchForm

    def get_initial(self):
        GET = self.request.GET
        initial = {
            'targeted_audiences': GET.getlist('targeted_audiences', ''),
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
            'targeted_audiences': GET.getlist('targeted_audiences', ''),
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


class AdvancedSearch(SearchMixin, FormView):
    """Step 5 of the multi-page search form."""

    template_name = 'search/step_advanced_search.html'
    form_class = AdvancedSearchForm

    def get_initial(self):
        GET = self.request.GET
        initial = {
            'targeted_audiences': GET.getlist('targeted_audiences', ''),
            'perimeter': GET.get('perimeter', ''),
            'themes': GET.getlist('themes', []),
            'categories': GET.getlist('categories', []),
        }
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        initial = self.get_initial()
        filter_form = AidSearchForm(initial)
        aids = filter_form.filter_queryset()

        context['total_aids'] = aids \
            .values('id') \
            .distinct() \
            .count()
        
        return context


class ProjectSearch(SearchMixin, FormView):
    """Step 6 of the multi-page search form."""

    template_name = 'search/step_project.html'
    form_class = ProjectSearchForm

    def get_initial(self):
        GET = self.request.GET
        initial = {
            'targeted_audiences': GET.getlist('targeted_audiences', ''),
            'perimeter': GET.get('perimeter', ''),
            'themes': GET.getlist('themes', []),
            'categories': GET.getlist('categories', []),
        }
        return initial
