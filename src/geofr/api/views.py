from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity

from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema

from core.utils import remove_accents
from core.api.pagination import ApiPagination
from geofr.models import Perimeter
from geofr.api import doc as api_doc
from geofr.api.serializers import PerimeterSerializer, PerimeterScaleSerializer


MIN_SEARCH_LENGTH = 1


class PerimeterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PerimeterSerializer
    pagination_class = ApiPagination

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

    @extend_schema(
        summary="Lister tous les périmètres",
        description="Si vous cherchez une API Adresse : \
        https://api.gouv.fr/les-api/base-adresse-nationale",
        parameters=api_doc.perimeters_api_parameters,
        tags=[Perimeter._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class PerimeterScalesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PerimeterScaleSerializer

    def get_queryset(self):
        perimeter_scales = [{'id': id, 'name': name, 'weight': weight} for (weight, id, name) in Perimeter.SCALES_TUPLE]  # noqa
        return perimeter_scales

    @extend_schema(
        summary="Lister tous les choix d'échelles",
        description="Ils sont ordonnés du plus petit au plus grand.",
        tags=[Perimeter._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)
