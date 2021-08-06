from rest_framework import routers

from aids.api.views import (
    AidViewSet,
    AidAudiences, AidTypes, AidSteps, AidRecurrences, AidDestinations)


router = routers.SimpleRouter()
router.register(r'audiences', AidAudiences, basename='aid-audiences')
router.register(r'types', AidTypes, basename='aid-types')
router.register(r'steps', AidSteps, basename='aid-steps')
router.register(r'recurrences', AidRecurrences, basename='aid-recurrences')
router.register(r'destinations', AidDestinations, basename='aid-destinations')
router.register('', AidViewSet, basename='aids')


urlpatterns = router.urls
