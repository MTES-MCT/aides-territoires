from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema

from core.api.pagination import ApiPagination
from programs.models import Program
from programs.api.serializers import ProgramSerializer


class ProgramViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all().order_by('id')
    pagination_class = ApiPagination

    @extend_schema(
        summary="Lister tous les programmes d'aides",
        tags=[Program._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)
