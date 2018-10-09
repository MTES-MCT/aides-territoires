from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from bundles.models import Bundle


class BundleListView(LoginRequiredMixin, ListView):
    """List user bundles."""

    template_name = 'bundles/list.html'
    context_object_name = 'bundles'

    def get_queryset(self):
        return Bundle.objects \
            .filter(owner=self.request.user)
