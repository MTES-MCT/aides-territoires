from rest_framework import viewsets, mixins

from core.utils import get_subdomain_from_host
from stats.models import AidMatchProjectEvent, AidEligibilityTestEvent
from stats.api.serializers import (AidMatchProjectEventSerializer,
                                   AidEligibilityTestEventSerializer)


class AidMatchProjectEventViewSet(mixins.CreateModelMixin,
                                  viewsets.GenericViewSet):
    queryset = AidMatchProjectEvent.objects.all()
    serializer_class = AidMatchProjectEventSerializer

    def perform_create(self, serializer):
        host = self.request.get_host()
        source_cleaned = get_subdomain_from_host(host)
        serializer.save(source=source_cleaned)


class AidEligibilityTestEventViewSet(mixins.CreateModelMixin,
                                     viewsets.GenericViewSet):
    queryset = AidEligibilityTestEvent.objects.all()
    serializer_class = AidEligibilityTestEventSerializer

    def perform_create(self, serializer):
        host = self.request.get_host()
        source_cleaned = get_subdomain_from_host(host)
        serializer.save(source=source_cleaned)
