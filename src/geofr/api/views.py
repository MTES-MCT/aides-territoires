from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity

from rest_framework import viewsets, mixins
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.utils import remove_accents
from geofr.models import Perimeter
from geofr.api.serializers import PerimeterSerializer, PerimeterScaleSerializer


MIN_SEARCH_LENGTH = 1

q_param = openapi.Parameter(
    'q',
    openapi.IN_QUERY,
    description="""
    Rechercher par nom.
    Il est possible d'avoir des résultats pertinents avec seulement le début du nom, \
    ou un nom légerement erroné.
    
    Exemples : 'lyon', 'par', 'grenble'
    """,
    type=openapi.TYPE_STRING)
scale_param = openapi.Parameter(
    'scale',
    openapi.IN_QUERY,
    description="""
    Filtrer par l'échelle.
    
    Exemple : 'department'
    """,
    type=openapi.TYPE_STRING)
# is_visible_to_users_param = openapi.Parameter(
#     'is_visible_to_users',
#     openapi.IN_QUERY,
#     description="Afficher les périmètres cachés. Exemple : 'true'",
#     type=openapi.TYPE_BOOLEAN)


class PerimeterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Lister tous les périmètres.

    Si vous cherchez une API Adresse : https://api.gouv.fr/les-api/base-adresse-nationale
    """
    serializer_class = PerimeterSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Perimeter.objects.order_by('-scale', 'name')

        accented_q = self.request.query_params.get('q', '')
        q = remove_accents(accented_q)

        if len(q) >= MIN_SEARCH_LENGTH:
            qs = qs \
                .annotate(similarity=TrigramSimilarity('unaccented_name', q)) \
                .filter(Q(unaccented_name__trigram_similar=remove_accents(q))
                        | Q(zipcodes__icontains=accented_q)) \
                .order_by('-similarity', '-scale', 'name')

        scale = self.request.query_params.get('scale', '')
        scale_weight = getattr(Perimeter.SCALES, scale, 0)
        if scale:
            qs = qs.filter(scale=scale_weight)

        is_visible_to_users = self.request.query_params.get('is_visible_to_users', 'false')  # noqa
        if is_visible_to_users == 'true':
            qs = qs.filter(is_visible_to_users=True)

        return qs

    @swagger_auto_schema(manual_parameters=[q_param, scale_param])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class PerimeterScalesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Lister tous les choix d'échelles.

    Ils sont ordonnés du plus petit au plus grand.
    """

    serializer_class = PerimeterScaleSerializer

    def get_queryset(self):
        perimeter_scales = [{'id': id, 'name': name, 'weight': weight} for (weight, id, name) in Perimeter.SCALES_TUPLE]  # noqa
        return perimeter_scales
