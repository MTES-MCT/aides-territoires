from django.db.models import Prefetch

from rest_framework import viewsets, mixins

from categories.models import Theme, Category
from categories.api.serializers import ThemeSerializer


class ThemeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Lister toutes les thématiques (avec leur liste de sous-thématiques).

    .
    """

    serializer_class = ThemeSerializer
    queryset = Theme.objects.all() \
        .prefetch_related(Prefetch('categories', queryset=Category.objects.all().order_by('id'))) \
        .order_by('id')
