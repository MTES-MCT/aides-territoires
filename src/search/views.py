from django.views.generic import FormView

from search.forms import AudianceSearchForm


class AudianceSearch(FormView):
    template_name = 'search/step_audiance.html'
    form_class = AudianceSearchForm
