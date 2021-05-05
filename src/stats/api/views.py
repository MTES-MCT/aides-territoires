from rest_framework import viewsets, mixins

from core.utils import get_site_from_host
from stats.models import (AidContactClickEvent,
                          AidMatchProjectEvent, AidEligibilityTestEvent)
from stats.api.serializers import (AidContactClickEventSerializer,
                                   AidMatchProjectEventSerializer,
                                   AidEligibilityTestEventSerializer)


class AidContactClickEventViewSet(mixins.CreateModelMixin,
                                  viewsets.GenericViewSet):
    queryset = AidContactClickEvent.objects.all()
    serializer_class = AidContactClickEventSerializer

    def perform_create(self, serializer):
        host = self.request.get_host()
        source_cleaned = get_subdomain_from_host(host)
        serializer.save(source=source_cleaned)


class AidMatchProjectEventViewSet(mixins.CreateModelMixin,
                                  viewsets.GenericViewSet):
    queryset = AidMatchProjectEvent.objects.all()
    serializer_class = AidMatchProjectEventSerializer

    def perform_create(self, serializer):
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        serializer.save(source=source_cleaned)


class AidEligibilityTestEventViewSet(mixins.CreateModelMixin,
                                     viewsets.GenericViewSet):
    queryset = AidEligibilityTestEvent.objects.all()
    serializer_class = AidEligibilityTestEventSerializer

    def perform_create(self, serializer):
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        serializer.save(source=source_cleaned)
