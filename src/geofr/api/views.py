from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity

from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema

from core.utils import remove_accents
from core.api.pagination import ApiPagination
from geofr.models import Perimeter, PerimeterData
from geofr.api import doc as api_doc
from geofr.api.serializers import (
    PerimeterDataSerializer,
    PerimeterSerializer,
    PerimeterScaleSerializer,
)

MIN_SEARCH_LENGTH = 1


class PerimeterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PerimeterSerializer
    pagination_class = ApiPagination

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Perimeter.objects.order_by("-scale", "name")

        accented_q = self.request.query_params.get("q", "")
        q = remove_accents(accented_q)

        scale = self.request.query_params.get("scale", "")
        if scale:
            # The scale parameter allows several values
            scales = scale.split(",")
            scale_weights = []
            for s in scales:
                scale_weights.append(getattr(Perimeter.SCALES, s, 0))

            if len(scale_weights) == 1:
                qs = qs.filter(scale=scale_weights[0])
            elif len(scale_weights) > 1:
                qs = qs.filter(scale__in=scale_weights)

        is_visible_to_users = self.request.query_params.get(
            "is_visible_to_users", "false"
        )  # noqa
        if is_visible_to_users == "true":
            qs = qs.filter(is_visible_to_users=True)

        is_non_obsolete = self.request.query_params.get(
            "is_non_obsolete", "true"
        )  # noqa
        if is_non_obsolete == "true":
            qs = qs.filter(is_obsolete=False)

        if len(q) >= MIN_SEARCH_LENGTH:
            qs = (
                qs.annotate(similarity=TrigramSimilarity("unaccented_name", q))
                .filter(
                    Q(unaccented_name__trigram_similar=remove_accents(q))
                    | Q(zipcodes__icontains=accented_q)
                )
                .order_by("-similarity", "-scale", "name")
            )

        return qs

    @extend_schema(
        summary="Lister tous les périmètres",
        description="Si vous cherchez une API Adresse : \
        https://api.gouv.fr/les-api/base-adresse-nationale",
        parameters=api_doc.perimeters_api_parameters,
        tags=[Perimeter._meta.verbose_name_plural],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class PerimeterDataViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PerimeterDataSerializer

    def get_queryset(self):
        qs = PerimeterData.objects.all()
        perimeter_id = self.request.query_params.get("perimeter_id", "")
        qs = qs.filter(perimeter__id=perimeter_id)

        return qs

    @extend_schema(
        summary="Lister les données supplémentaires sur un périmètre",
        description="Utilisé pour des périmètres de commune uniquement.",
        parameters=api_doc.perimeterdata_api_parameters,
        tags=[Perimeter._meta.verbose_name_plural],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class PerimeterScalesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PerimeterScaleSerializer

    def get_queryset(self):
        perimeter_scales = [
            {"id": id, "name": name, "weight": weight}
            for (weight, id, name) in Perimeter.SCALES_TUPLE
        ]  # noqa
        return perimeter_scales

    @extend_schema(
        summary="Lister tous les choix d'échelles",
        description="Ils sont ordonnés du plus petit au plus grand.",
        tags=[Perimeter._meta.verbose_name_plural],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)
