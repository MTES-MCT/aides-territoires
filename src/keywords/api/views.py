from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import F
from django.contrib.postgres.search import SearchRank

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from core.utils import remove_accents, parse_query
from core.api.pagination import ApiPagination
from keywords.models import SynonymList
from keywords.api.serializers import SynonymListSerializer, SynonymClassicListSerializer


def noop_decorator(func):
    """
    We use this "noop" decorator in order to disable caching.
    """
    return func


cache_list_page = noop_decorator
if settings.ENABLE_OTHER_LIST_API_CACHE:
    timeout = settings.OTHER_LIST_API_CACHE_TIMEOUT
    cache_list_page = method_decorator(cache_page(timeout))


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

    @cache_list_page
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @cache_list_page
    @action(detail=False, url_path="classic-list", url_name="classic")
    def classic_list(self, request):
        classic = self.get_queryset()
        classic_serializer = SynonymClassicListSerializer(classic, many=True).data
        return Response(classic_serializer)
