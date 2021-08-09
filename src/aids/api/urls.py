from rest_framework import routers

from aids.api.views import (
    AidViewSet,
    AidAudiencesViewSet, AidTypesViewSet, AidStepsViewSet, AidRecurrencesViewSet, AidDestinationsViewSet)  # noqa


router = routers.SimpleRouter()
router.register(r'audiences', AidAudiencesViewSet, basename='aid-audiences')
router.register(r'types', AidTypesViewSet, basename='aid-types')
router.register(r'steps', AidStepsViewSet, basename='aid-steps')
router.register(r'recurrences', AidRecurrencesViewSet, basename='aid-recurrences')
router.register(r'destinations', AidDestinationsViewSet, basename='aid-destinations')
router.register('', AidViewSet, basename='aids')


urlpatterns = router.urls
