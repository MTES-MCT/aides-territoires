import operator
from functools import reduce

from django.db.models import Q

from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema

from core.api.pagination import ApiPagination
from keywords.models import SynonymList
from keywords.api.serializers import SynonymListSerializer


MIN_SEARCH_LENGTH = 2


class SynonymListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SynonymListSerializer
    pagination_class = ApiPagination

    def get_queryset(self):
        """Filter data according to search query."""

        qs = SynonymList.objects.all()

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

    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)
