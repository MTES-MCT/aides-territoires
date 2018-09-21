from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormMixin

from aids.models import Aid
from aids.forms import AidSearchForm, AidCreateForm
from geofr.models import Perimeter


class SearchView(FormMixin, ListView):
    """Search and display aids."""

    template_name = 'aids/search.html'
    context_object_name = 'aids'
    paginate_by = 20
    form_class = AidSearchForm

    def get_selected_perimeter(self):
        if not hasattr(self, 'perimeter'):
            perimeter_slug = self.request.GET.get('perimeter', '')
            perimeter_id = perimeter_slug.split('-')[0]
            if perimeter_id:
                try:
                    self.perimeter = Perimeter.objects.get(pk=perimeter_id)
                except Perimeter.DoesNotExist:
                    self.perimeter = None
            else:
                self.perimeter = None

        return self.perimeter

    def get_form_kwargs(self):
        """Take input data from the GET values."""

        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':

            # Clean the "perimeter" field value: removes the slug before
            # sending data to the form
            mutable_GET = self.request.GET.copy()
            if 'perimeter' in self.request.GET:
                perimeter_slug = self.request.GET.get('perimeter')
                perimeter_id = perimeter_slug.split('-')[0]
                mutable_GET['perimeter'] = perimeter_id

            kwargs.update({
                'data': mutable_GET,
                'perimeter': self.get_selected_perimeter(),
            })

        return kwargs

    def get_queryset(self):
        """Return the list of results to display."""

        qs = Aid.objects \
            .published() \
            .open() \
            .select_related('perimeter') \
            .prefetch_related('backers') \
            .order_by('perimeter__scale', 'submission_deadline')

        filter_form = self.get_form()
        results = filter_form.filter_queryset(qs)
        return results


class AidCreateView(CreateView):
    """Allows publishers to submit their own aids."""

    template_name = 'aids/create.html'
    form_class = AidCreateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
