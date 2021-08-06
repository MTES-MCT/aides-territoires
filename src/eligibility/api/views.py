from rest_framework import viewsets, mixins

from eligibility.models import EligibilityTest
from eligibility.api.serializers import EligibilityTestSerializer


class EligibilityTestViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = EligibilityTestSerializer
    queryset = EligibilityTest.objects.all()
