from django.views.generic import FormView

from search.forms import AudianceSearchForm, PerimeterSearchForm


class AudianceSearch(FormView):
    template_name = 'search/step_audiance.html'
    form_class = AudianceSearchForm

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class PerimeterSearch(FormView):
    template_name = 'search/step_perimeter.html'
    form_class = PerimeterSearchForm

    def get_initial(self):
        initial = super().get_initial()
        initial['targeted_audiances'] = \
            self.request.GET.get('targeted_audiances', None)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['querystring'] = self.request.GET.urlencode()
        return context
