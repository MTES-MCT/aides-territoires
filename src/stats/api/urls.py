from rest_framework import routers

from stats.api.views import (AidContactClickEventViewSet,
                             AidMatchProjectEventViewSet,
                             AidEligibilityTestEventViewSet,
                             PromotionClickEventViewSet)


router = routers.SimpleRouter()
router.register(r'aid-contact-click-events', AidContactClickEventViewSet,
                basename='aid-contact-click-events')
router.register(r'aid-match-project-events', AidMatchProjectEventViewSet,
                basename='aid-match-project-events')
router.register(r'aid-eligibility-test-events', AidEligibilityTestEventViewSet,
                basename='aid-eligibility-test-events')
router.register(r'promotion-click-events', PromotionClickEventViewSet,
                basename='promotion-click-events')


urlpatterns = router.urls
