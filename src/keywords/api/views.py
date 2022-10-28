from core.utils import remove_accents, parse_query

from django.db.models import F
from django.contrib.postgres.search import SearchRank

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from core.api.pagination import ApiPagination
from keywords.models import SynonymList
from keywords.api.serializers import SynonymListSerializer, SynonymClassicListSerializer


class SynonymListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SynonymListSerializer
    pagination_class = ApiPagination

    def get_queryset(self):
        """Filter data according to search query."""

        qs = SynonymList.objects.all()

        terms = self.request.query_params.get("q", "")

        if terms:
            terms = self.request.query_params.get("q", "")
            query = parse_query(remove_accents(terms))
            qs = qs.filter(search_vector_keywords_list=query).annotate(
                rank=SearchRank(F("search_vector_keywords_list"), query)
            )

        qs = qs.order_by("name").distinct()

        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @action(detail=False, url_path="classic-list", url_name="classic")
    def classic_list(self, request):
        classic = self.get_queryset()
        classic_serializer = SynonymClassicListSerializer(classic, many=True).data
        return Response(classic_serializer)
