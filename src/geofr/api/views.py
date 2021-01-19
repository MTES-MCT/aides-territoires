import unicodedata
from rest_framework import viewsets
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.lookups import Unaccent

from geofr.models import Perimeter
from geofr.api.serializers import PerimeterSerializer


MIN_SEARCH_LENGTH = 1


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


class PerimeterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerimeterSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Perimeter.objects.order_by('-scale', 'name')
        q = self.request.query_params.get('q', '')
        if len(q) >= MIN_SEARCH_LENGTH:
            qs = qs \
                .annotate(similarity=TrigramSimilarity(Unaccent('name'), q)) \
                .filter(name__unaccent__trigram_similar=remove_accents(q)) \
                .order_by('-similarity', '-scale', 'name')

        return qs
