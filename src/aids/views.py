from django.views.generic import ListView

from aids.models import Aid


class SearchView(ListView):
    """Search and display aids."""

    template_name = 'aids/search.html'
    context_object_name = 'aids'
    paginate_by = 20

    def get_queryset(self):
        qs = Aid.objects \
            .published() \
            .select_related('backer') \
            .order_by('-id')
        return qs
