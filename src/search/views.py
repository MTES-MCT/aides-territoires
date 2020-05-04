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
    template_name = 'search/step_audiance.html'
    form_class = AudianceSearchForm


class PerimeterSearch(SearchMixin, FormView):
    template_name = 'search/step_perimeter.html'
    form_class = PerimeterSearchForm

    def get_initial(self):
        GET = self.request.GET
        initial = {
            'targeted_audiances': GET.getlist('targeted_audiances', ''),
        }
        return initial


class ThemeSearch(SearchMixin, FormView):
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
        aids = filter_form.filter_queryset()
        theme_aids = aids.filter(categories__theme__slug__in=initial['themes'])
        context['total_aids'] = theme_aids.count()
        return context


class SearchPageDetail(SearchView):
    template_name = 'search/search_page.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self):
        qs = SearchPage.objects.filter(slug=self.kwargs.get('slug'))
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
