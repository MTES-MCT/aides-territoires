from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from bundles.forms import BundleCreateForm
from bundles.models import Bundle


class BundleViewMixin:

    def get_bundles(self):
        return Bundle.objects \
            .filter(owner=self.request.user) \
            .select_related('owner') \
            .order_by('name')


class BundleListView(LoginRequiredMixin, BundleViewMixin, ListView):
    """List user bundles."""

    template_name = 'bundles/list.html'
    context_object_name = 'bundles'

    def get_queryset(self):
        return self.get_bundles()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        if slug:
            bundle = get_object_or_404(self.object_list, slug=slug)
            context['selected_bundle'] = bundle
            context['aids'] = bundle.aids \
                .published() \
                .select_related('author') \
                .prefetch_related('backers')
        return context


class BundleCreateView(LoginRequiredMixin, BundleViewMixin, CreateView):
    """Create new bundles."""

    template_name = 'bundles/create.html'
    form_class = BundleCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bundles'] = self.get_bundles()
        return context

    def form_valid(self, form):
        bundle = form.save(commit=False)
        bundle.owner = self.request.user
        bundle.save()

        msg = _('The new bundle was created successfuly')
        messages.success(self.request, msg)
        success_url = reverse('bundle_list_view', args=[bundle.slug])
        return HttpResponseRedirect(success_url)
