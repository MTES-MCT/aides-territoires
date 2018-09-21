import operator
from functools import reduce
from rest_framework import viewsets
from django.db.models import Q

from backers.models import Backer
from backers.api.serializers import BackerSerializer


MIN_SEARCH_LENGTH = 3


class BackerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BackerSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Backer.objects.all()
        q = self.request.query_params.get('q', '')
        terms = q.split()
        q_filters = []
        for term in terms:
            if len(term) >= MIN_SEARCH_LENGTH:
                q_filters.append(Q(name__icontains=term))

        if q_filters:
            qs = qs.filter(reduce(operator.and_, q_filters))

        qs = qs.order_by('name')

        return qs
