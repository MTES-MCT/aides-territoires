from rest_framework import viewsets

from geofr.models import Perimeter
from geofr.api.serializers import PerimeterSerializer


MIN_SEARCH_LENGTH = 3


class PerimeterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerimeterSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Perimeter.objects.all()
        q = self.request.query_params.get('q', None)
        if q is not None and len(q) >= MIN_SEARCH_LENGTH:
            qs = qs.filter(name__icontains=q)

        return qs
