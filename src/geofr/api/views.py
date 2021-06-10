from rest_framework import viewsets
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q

from geofr.models import Perimeter, remove_accents
from geofr.api.serializers import PerimeterSerializer


MIN_SEARCH_LENGTH = 1


class PerimeterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerimeterSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Perimeter.objects.order_by('-scale', 'name')

        accented_q = self.request.query_params.get('q', '')
        q = remove_accents(accented_q)

        if len(q) >= MIN_SEARCH_LENGTH:
            qs = qs \
                .annotate(similarity=TrigramSimilarity('unaccented_name', q)) \
                .filter(Q(unaccented_name__trigram_similar=remove_accents(q))
                        | Q(zipcodes__icontains=accented_q)) \
                .order_by('-similarity', '-scale', 'name')

        is_visible_to_users = self.request.query_params.get('is_visible_to_users', 'false')  # noqa
        if is_visible_to_users == 'true':
            qs = qs.filter(is_visible_to_users=True)

        return qs
