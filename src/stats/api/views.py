from rest_framework import viewsets, mixins

from core.utils import get_subdomain_from_host
from stats.models import AidMatchProjectEvent
from stats.api.serializers import AidMatchProjectEventSerializer


class AidMatchProjectEventViewSet(mixins.CreateModelMixin,
                                     viewsets.GenericViewSet):
    queryset = AidMatchProjectEvent.objects.all()
    serializer_class = AidMatchProjectEventSerializer

    def perform_create(self, serializer):
        print(self.request.data)
        host = self.request.get_host()
        source_cleaned = get_subdomain_from_host(host)
        serializer.save(source=source_cleaned)