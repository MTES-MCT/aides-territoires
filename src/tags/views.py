from django.views.generic import ListView
from django.db.models import Count

from tags.models import Tag


class TagListView(ListView):
    """Display the list of known tags on a single page."""

    template_name = 'tags/list.html'
    context_object_name = 'tags'
    paginate_by = 96

    def get_queryset(self):
        qs = Tag.objects \
            .filter(aids__status='published') \
            .annotate(nb_aids=Count('aids')) \
            .order_by('-nb_aids', 'name')
        return qs
