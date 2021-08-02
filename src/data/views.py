from django.views.generic import TemplateView
from django.conf import settings


class DataDocView(TemplateView):
    """Show aids api doc and licence."""

    template_name = 'data/doc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_version'] = settings.CURRENT_API_VERSION
        return context
