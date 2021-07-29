from rest_framework import viewsets, mixins

from programs.models import Program
from programs.api.serializers import ProgramSerializer


class ProgramViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()
