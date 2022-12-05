from rest_framework import routers

from stats.api.views import (
    AccountRegisterFromNextpagewarningClickEventViewSet,
    AidContactClickEventViewSet,
    AidOriginUrlClickEventViewSet,
    AidApplicationUrlClickEventViewSet,
    AidEligibilityTestEventViewSet,
    PromotionDisplayEventViewSet,
    PromotionClickEventViewSet,
)


router = routers.SimpleRouter()
router.register(
    r"account-register-from-nextpagewarning-click-events",
    AccountRegisterFromNextpagewarningClickEventViewSet,
    basename="account-register-from-nextpagewarning-click-events",
)
router.register(
    r"aid-contact-click-events",
    AidContactClickEventViewSet,
    basename="aid-contact-click-events",
)
router.register(
    r"aid-originurl-click-events",
    AidOriginUrlClickEventViewSet,
    basename="aid-originurl-click-events",
)
router.register(
    r"aid-applicationurl-click-events",
    AidApplicationUrlClickEventViewSet,
    basename="aid-applicationurl-click-events",
)
router.register(
    r"aid-eligibility-test-events",
    AidEligibilityTestEventViewSet,
    basename="aid-eligibility-test-events",
)
router.register(
    r"promotion-display-events",
    PromotionDisplayEventViewSet,
    basename="promotion-display-events",
)
router.register(
    r"promotion-click-events",
    PromotionClickEventViewSet,
    basename="promotion-click-events",
)

urlpatterns = router.urls
