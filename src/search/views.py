from django.views.generic import FormView

from search.forms import (AudianceSearchForm, PerimeterSearchForm,
                          ThemeSearchForm)


class AudianceSearch(FormView):
    template_name = 'search/step_audiance.html'
    form_class = AudianceSearchForm

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class PerimeterSearch(FormView):
    template_name = 'search/step_perimeter.html'
    form_class = PerimeterSearchForm

    def get_initial(self):
        return self.request.GET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['querystring'] = self.request.GET.urlencode()
        return context


class ThemeSearch(FormView):
    template_name = 'search/step_theme.html'
    form_class = ThemeSearchForm

    def get_initial(self):
        return self.request.GET
