from rest_framework import viewsets
from django.contrib.postgres.search import TrigramSimilarity

from geofr.models import Perimeter
from geofr.api.serializers import PerimeterSerializer


MIN_SEARCH_LENGTH = 1


class PerimeterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerimeterSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Perimeter.objects.order_by('-scale', 'name')
        q = self.request.query_params.get('q', '')
        if len(q) >= MIN_SEARCH_LENGTH:
            qs = qs \
                .annotate(similarity=TrigramSimilarity('name__unaccent', q)) \
                .filter(name__unaccent__trigram_similar=q) \
                .order_by('-similarity', '-scale', 'name')

        return qs
