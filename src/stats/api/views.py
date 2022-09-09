from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema

from core.utils import get_site_from_host
from search.utils import clean_search_querystring
from stats.models import (
    AidContactClickEvent,
    AidOriginUrlClickEvent,
    AidApplicationUrlClickEvent,
    AidEligibilityTestEvent,
    PromotionDisplayEvent,
    PromotionClickEvent,
)
from stats.api.serializers import (
    AidContactClickEventSerializer,
    AidOriginUrlClickEventSerializer,
    AidApplicationUrlClickEventSerializer,
    AidEligibilityTestEventSerializer,
    PromotionClickEventSerializer,
    PromotionDisplayEventSerializer,
)


@extend_schema(exclude=True)
class AidContactClickEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AidContactClickEventSerializer
    queryset = AidContactClickEvent.objects.all()

    def perform_create(self, serializer):
        # clean host
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        # clean querystring
        querystring = serializer.validated_data.get("querystring")
        querystring_cleaned = clean_search_querystring(querystring)
        # save
        serializer.save(source=source_cleaned, querystring=querystring_cleaned)


@extend_schema(exclude=True)
class AidOriginUrlClickEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AidOriginUrlClickEventSerializer
    queryset = AidOriginUrlClickEvent.objects.all()

    def perform_create(self, serializer):
        # clean host
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        # clean querystring
        querystring = serializer.validated_data.get("querystring")
        querystring_cleaned = clean_search_querystring(querystring)
        # save
        serializer.save(source=source_cleaned, querystring=querystring_cleaned)


@extend_schema(exclude=True)
class AidApplicationUrlClickEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AidApplicationUrlClickEventSerializer
    queryset = AidApplicationUrlClickEvent.objects.all()

    def perform_create(self, serializer):
        # clean host
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        # clean querystring
        querystring = serializer.validated_data.get("querystring")
        querystring_cleaned = clean_search_querystring(querystring)
        # save
        serializer.save(source=source_cleaned, querystring=querystring_cleaned)


@extend_schema(exclude=True)
class AidEligibilityTestEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AidEligibilityTestEventSerializer
    queryset = AidEligibilityTestEvent.objects.all()

    def perform_create(self, serializer):
        # clean host
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        # clean querystring
        querystring = serializer.validated_data.get("querystring")
        querystring_cleaned = clean_search_querystring(querystring)
        # save
        serializer.save(source=source_cleaned, querystring=querystring_cleaned)


@extend_schema(exclude=True)
class PromotionDisplayEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PromotionDisplayEventSerializer
    queryset = PromotionDisplayEvent.objects.all()

    def perform_create(self, serializer):
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        serializer.save(source=source_cleaned)


@extend_schema(exclude=True)
class PromotionClickEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PromotionClickEventSerializer
    queryset = PromotionClickEvent.objects.all()

    def perform_create(self, serializer):
        host = self.request.get_host()
        source_cleaned = get_site_from_host(host)
        serializer.save(source=source_cleaned)
