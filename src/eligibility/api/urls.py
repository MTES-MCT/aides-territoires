from rest_framework import routers

from eligibility.api.views import EligibilityTestViewSet


router = routers.SimpleRouter()
router.register("", EligibilityTestViewSet, basename="eligibility")


urlpatterns = router.urls
