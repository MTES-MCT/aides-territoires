from rest_framework import routers

from stats.api.views import (AidContactClickEventViewSet,
                             AidMatchProjectEventViewSet,
                             AidEligibilityTestEventViewSet)


router = routers.SimpleRouter()
router.register(r'aid-contact-click-events', AidContactClickEventViewSet,
                basename='aid-contact-click-events')
router.register(r'aid-match-project-events', AidMatchProjectEventViewSet,
                basename='aid-match-project-events')
router.register(r'aid-eligibility-test-events', AidEligibilityTestEventViewSet,
                basename='aid-eligibility-test-events')


urlpatterns = router.urls
