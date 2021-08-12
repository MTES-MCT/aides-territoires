from rest_framework import viewsets, mixins

from eligibility.models import EligibilityTest
from eligibility.api.serializers import EligibilityTestSerializer


# mixins.ListModelMixin
class EligibilityTestViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    swagger_schema = None
    serializer_class = EligibilityTestSerializer
    queryset = EligibilityTest.objects.all()
