from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from aids.models import Aid
from aids.forms import AidSearchForm, AidCreateForm


class SearchView(FormMixin, ListView):
    """Search and display aids."""

    template_name = 'aids/search.html'
    context_object_name = 'aids'
    paginate_by = 20
    form_class = AidSearchForm

    def get_form_kwargs(self):
        """Take input data from the GET values."""

        kwargs = super().get_form_kwargs()
        kwargs.update({
            'data': self.request.GET,
        })

        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['integration'] = self.request.GET.get('integration', False)
        return super().get_context_data(**kwargs)

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


class ResultsView(SearchView):
    """Only display search results.

    This view is designed to be called via ajax, and only renders html
    fragment of search engine results.
    """
    template_name = 'aids/_results.html'

    def get_context_data(self, **kwargs):
        kwargs['search_actions'] = True
        return super().get_context_data(**kwargs)


class AidCreateView(SuccessMessageMixin, CreateView):
    """Allows publishers to submit their own aids."""

    template_name = 'aids/create.html'
    form_class = AidCreateForm
    success_url = reverse_lazy('aid_create_view')
    success_message = _('Your aid was sucessfully created. \
                        It will be reviewed by an admin soon.')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form


class AidDetailView(DetailView):
    """Display an aid detail."""

    template_name = 'aids/detail.html'

    def get_queryset(self):
        qs = Aid.objects \
            .published() \
            .open() \
            .select_related('perimeter') \
            .prefetch_related('backers')
        return qs
