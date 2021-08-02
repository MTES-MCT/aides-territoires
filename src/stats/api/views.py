from rest_framework import viewsets, mixins

from core.utils import get_site_from_host
from search.utils import clean_search_querystring
from stats.models import (AidContactClickEvent,
                          AidMatchProjectEvent, AidEligibilityTestEvent,
                          PromotionDisplayEvent, PromotionClickEvent)
from stats.api.serializers import (AidContactClickEventSerializer,
                                   AidMatchProjectEventSerializer,
                                   AidEligibilityTestEventSerializer,
                                   PromotionClickEventSerializer,
                                   PromotionDisplayEventSerializer,)


class AidContactClickEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    swagger_schema = None
    queryset = AidContactClickEvent.objects.all()
    serializer_class = AidContactClickEventSerializer

    def perform_create(self, serializer):
        # clean host
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        # clean querystring
        querystring = serializer.validated_data.get('querystring')
        querystring_cleaned = clean_search_querystring(querystring)
        # save
        serializer.save(source=source_cleaned, querystring=querystring_cleaned)


class AidMatchProjectEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    swagger_schema = None
    queryset = AidMatchProjectEvent.objects.all()
    serializer_class = AidMatchProjectEventSerializer

    def perform_create(self, serializer):
        # clean host
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        # clean querystring
        querystring = serializer.validated_data.get('querystring')
        querystring_cleaned = clean_search_querystring(querystring)
        # save
        serializer.save(source=source_cleaned, querystring=querystring_cleaned)


class AidEligibilityTestEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    swagger_schema = None
    queryset = AidEligibilityTestEvent.objects.all()
    serializer_class = AidEligibilityTestEventSerializer

    def perform_create(self, serializer):
        # clean host
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        # clean querystring
        querystring = serializer.validated_data.get('querystring')
        querystring_cleaned = clean_search_querystring(querystring)
        # save
        serializer.save(source=source_cleaned, querystring=querystring_cleaned)


class PromotionDisplayEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    swagger_schema = None
    queryset = PromotionDisplayEvent.objects.all()
    serializer_class = PromotionDisplayEventSerializer

    def perform_create(self, serializer):
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        serializer.save(source=source_cleaned)


class PromotionClickEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    swagger_schema = None
    queryset = PromotionClickEvent.objects.all()
    serializer_class = PromotionClickEventSerializer

    def perform_create(self, serializer):
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        serializer.save(source=source_cleaned)
