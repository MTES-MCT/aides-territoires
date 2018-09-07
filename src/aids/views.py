from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from aids.models import Aid
from aids.forms import AidSearchForm
from geofr.models import Perimeter


class SearchView(FormMixin, ListView):
    """Search and display aids."""

    template_name = 'aids/search.html'
    context_object_name = 'aids'
    paginate_by = 20
    form_class = AidSearchForm

    def get_selected_perimeter(self):
        if not hasattr(self, 'perimeter'):
            perimeter_id = self.request.GET.get('perimeter', None)
            if perimeter_id:
                self.perimeter = Perimeter.objects.get(pk=perimeter_id)

        return self.perimeter

    def get_form_kwargs(self):
        """Take input data from the GET values."""

        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
                'perimeter': self.get_selected_perimeter(),
            })

        return kwargs

    def get_queryset(self):
        """Return the list of results to display."""

        qs = Aid.objects \
            .published() \
            .open() \
            .select_related('backer') \
            .order_by('-id')

        filter_form = self.get_form()
        results = filter_form.filter_queryset(qs)
        return results
