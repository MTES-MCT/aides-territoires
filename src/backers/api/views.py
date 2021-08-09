import operator
from functools import reduce

from django.db.models import Q

from rest_framework import viewsets, mixins
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from backers.models import Backer
from backers.api.serializers import BackerSerializer


MIN_SEARCH_LENGTH = 3

q_param = openapi.Parameter(
    'q',
    openapi.IN_QUERY,
    description="""
    Rechercher par nom.
    Il est possible d'avoir des résultats pertinents avec seulement le début du nom.

    Exemples : 'ademe', 'conseil régional'
    """,
    type=openapi.TYPE_STRING)
has_financed_aids_param = openapi.Parameter(
    'has_financed_aids',
    openapi.IN_QUERY,
    description="""
    Renvoyer seulement les porteurs d'aides avec des aides.

    Exemple : 'true'
    """,
    type=openapi.TYPE_BOOLEAN)
has_published_financed_aids_param = openapi.Parameter(
    'has_published_financed_aids',
    openapi.IN_QUERY,
    description="""
    Renvoyer seulement les porteurs d'aides avec des aides publiées.

    Exemple : 'true'
    """,
    type=openapi.TYPE_BOOLEAN)


class BackerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Lister tous les porteurs d'aides.

    .
    """

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

        has_financed_aids = self.request.query_params.get('has_financed_aids', 'false')
        if has_financed_aids == 'true':
            qs = qs.has_financed_aids()

        has_published_financed_aids = self.request.query_params.get('has_published_financed_aids', 'false')  # noqa
        if has_published_financed_aids == 'true':
            qs = qs.has_published_financed_aids()

        qs = qs.order_by('name')

        return qs

    @swagger_auto_schema(manual_parameters=[q_param, has_financed_aids_param, has_published_financed_aids_param])  # noqa
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)
