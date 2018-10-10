from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from bundles.models import Bundle


class BundleListView(LoginRequiredMixin, ListView):
    """List user bundles."""

    template_name = 'bundles/list.html'
    context_object_name = 'bundles'

    def get_queryset(self):
        return Bundle.objects \
            .filter(owner=self.request.user) \
            .select_related('owner') \
            .order_by('name')

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
