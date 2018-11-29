import operator
from functools import reduce
from rest_framework import viewsets
from django.db.models import Q

from geofr.models import Perimeter
from geofr.api.serializers import PerimeterSerializer


MIN_SEARCH_LENGTH = 1


class PerimeterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerimeterSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Perimeter.objects.all()
        q = self.request.query_params.get('q', '')
        terms = q.split()
        q_filters = []
        for term in terms:
            if len(term) >= MIN_SEARCH_LENGTH:
                q_filters.append(Q(name__icontains=term))

        if q_filters:
            qs = qs.filter(reduce(operator.and_, q_filters))

        qs = qs.order_by('-scale', 'name')

        return qs
