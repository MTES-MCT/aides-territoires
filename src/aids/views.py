from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormMixin
from django.urls import reverse

from aids.forms import AidEditForm, AidSearchForm
from aids.models import Aid


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


class ResultsReceiveView(LoginRequiredMixin, SearchView):
    """Send the search results by email."""

    http_method_names = ['post']
    EMAIL_SUBJECT = 'Vos résultats de recherche'

    def get_form_data(self):
        querydict = self.request.POST.copy()
        for key in ('csrfmiddlewaretoken', 'integration'):
            try:
                querydict.pop(key)
            except KeyError:
                pass
        return querydict

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.get_form_data()
        return kwargs

    def post(self, request, *args, **kwargs):
        """Send those search results by email to the user.

        We do it synchronously, but this view is meant to be called from an
        ajax query, so it should not be a problem.
        """

        results = self.get_queryset()
        nb_results = results.count()
        first_results = results[:10]
        site = get_current_site(self.request)
        querystring = self.get_form_data().urlencode()
        scheme = 'https' if self.request.is_secure() else 'http'
        search_url = reverse('search_view')
        full_url = '{scheme}://{domain}{search_url}?{querystring}'.format(
            scheme=scheme,
            domain=site.domain,
            search_url=search_url,
            querystring=querystring)
        results_body = render_to_string('emails/search_results.txt', {
            'user_name': self.request.user.full_name,
            'aids': first_results,
            'nb_results': nb_results,
            'full_url': full_url,
            'scheme': scheme,
            'domain': site.domain,
        })
        send_mail(
            self.EMAIL_SUBJECT,
            results_body,
            settings.DEFAULT_FROM_EMAIL,
            [self.request.user.email],
            fail_silently=False)
        return HttpResponse('')


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


class AidEditMixin:
    """Common code to aid editing views."""

    def get_queryset(self):
        qs = Aid.objects \
            .filter(author=self.request.user) \
            .order_by('name')
        return qs


class AidDraftListView(LoginRequiredMixin, AidEditMixin, ListView):
    """Display the list of aids published by the user."""

    template_name = 'aids/draft_list.html'
    context_object_name = 'aids'
    paginate_by = 30


class AidCreateView(LoginRequiredMixin, CreateView):
    """Allows publishers to submit their own aids."""

    template_name = 'aids/create.html'
    form_class = AidEditForm
    success_url = reverse_lazy('aid_draft_list_view')

    def form_valid(self, form):
        aid = form.save(commit=False)
        aid.author = self.request.user
        aid.save()
        form.save_m2m()

        edit_url = reverse('aid_edit_view', args=[aid.slug])
        msg = _('Your aid was sucessfully created. It will be reviewed \
                 by an admin soon. You can <a href="%(url)s">keep editing \
                 it</a>.') % {'url': edit_url}
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.success_url)


class AidEditView(LoginRequiredMixin, SuccessMessageMixin, AidEditMixin,
                  UpdateView):
    """Edit an existing aid."""

    template_name = 'aids/edit.html'
    context_object_name = 'aid'
    form_class = AidEditForm
    success_url = reverse_lazy('aid_draft_list_view')
    success_message = _('Your aid was sucessfully edited. \
                        It will be reviewed by an admin soon.')
