from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import viewsets

from tags.models import Tag
from tags.api.serializers import TagSerializer


MIN_SEARCH_LENGTH = 2


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Tag.objects.all()
        q = self.request.query_params.get('q', '')
        if len(q) >= MIN_SEARCH_LENGTH:
            qs = qs \
                .annotate(similarity=TrigramSimilarity('name', q)) \
                .filter(name__trigram_similar=q) \
                .order_by('-similarity', 'name')

        return qs
