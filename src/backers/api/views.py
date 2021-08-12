import operator
from functools import reduce

from django.db.models import Q

from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema

from core.api.pagination import ApiPagination
from backers.models import Backer
from backers.api import doc as api_doc
from backers.api.serializers import BackerSerializer


MIN_SEARCH_LENGTH = 3


class BackerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BackerSerializer
    pagination_class = ApiPagination

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

        has_financed_aids = self.request.query_params.get('has_financed_aids', 'false')
        if has_financed_aids == 'true':
            qs = qs.has_financed_aids()

        has_published_financed_aids = self.request.query_params.get('has_published_financed_aids', 'false')  # noqa
        if has_published_financed_aids == 'true':
            qs = qs.has_published_financed_aids()

        qs = qs.order_by('name')

        return qs

    @extend_schema(
        summary="Lister tous les porteurs d'aides",
        parameters=api_doc.backers_api_parameters,
        tags=[Backer._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)
