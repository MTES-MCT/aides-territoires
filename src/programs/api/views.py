from rest_framework import viewsets, mixins
from drf_yasg.utils import swagger_auto_schema

from core.api.pagination import ApiPagination
from programs.models import Program
from programs.api.serializers import ProgramSerializer


class ProgramViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list: Lister tous les programmes d'aides

    .
    """

    serializer_class = ProgramSerializer
    queryset = Program.objects.all().order_by('id')
    pagination_class = ApiPagination

    @swagger_auto_schema(tags=[Program._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)
