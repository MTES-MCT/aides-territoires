from rest_framework import viewsets, mixins

from eligibility.models import EligibilityTest
from eligibility.api.serializers import EligibilityTestSerializer


class EligibilityTestViewSet(mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    queryset = EligibilityTest.objects.all()
    serializer_class = EligibilityTestSerializer
