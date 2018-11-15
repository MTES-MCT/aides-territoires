import operator
from functools import reduce
from rest_framework import viewsets
from django.db.models import Q

from tags.models import Tag
from tags.api.serializers import TagSerializer


MIN_SEARCH_LENGTH = 3


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Tag.objects.all()
        q = self.request.query_params.get('q', '')
        terms = q.split()
        q_filters = []
        for term in terms:
            if len(term) >= MIN_SEARCH_LENGTH:
                q_filters.append(Q(name__contains=term.lower()))

        if q_filters:
            qs = qs.filter(reduce(operator.and_, q_filters))

        qs = qs.order_by('name')

        return qs
