from rest_framework import viewsets, mixins
from drf_yasg.utils import swagger_auto_schema

from eligibility.models import EligibilityTest
from eligibility.api.serializers import EligibilityTestSerializer


class EligibilityTestViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = EligibilityTestSerializer
    queryset = EligibilityTest.objects.all()

    @swagger_auto_schema(tags=[EligibilityTest._meta.verbose_name_plural])
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, args, kwargs)
