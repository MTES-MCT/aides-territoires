from django.views.generic import ListView

from aids.models import Aid


class SearchView(ListView):
    """Search and display aids."""

    template_name = 'aids/search.html'

    def get_queryset(self):
        qs = Aid.objects.all()
        return qs

