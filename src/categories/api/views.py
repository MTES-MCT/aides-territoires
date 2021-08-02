from rest_framework import viewsets, mixins

from categories.models import Theme
from categories.api.serializers import ThemeSerializer


class ThemeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()
