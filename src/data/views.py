from django.views.generic import TemplateView


class DataDocView(TemplateView):
    """Show aids api doc and licence."""

    template_name = 'data/doc.html'
