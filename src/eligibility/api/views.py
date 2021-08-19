from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema

from eligibility.models import EligibilityTest
from eligibility.api.serializers import EligibilityTestSerializer


@extend_schema(exclude=True)
class EligibilityTestViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = EligibilityTestSerializer
    queryset = EligibilityTest.objects.all()
