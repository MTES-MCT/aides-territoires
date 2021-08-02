import operator
from functools import reduce

from django.db.models import Q

from rest_framework import viewsets, mixins

from backers.models import Backer
from backers.api.serializers import BackerSerializer


MIN_SEARCH_LENGTH = 3


class BackerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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

        has_financed_aids = self.request.query_params.get('has_financed_aids', 'false')  # noqa
        if has_financed_aids == 'true':
            qs = qs.has_financed_aids()

        has_published_financed_aids = self.request.query_params.get('has_published_financed_aids', 'false')  # noqa
        if has_published_financed_aids == 'true':
            qs = qs.has_published_financed_aids()

        qs = qs.order_by('name')

        return qs
