from rest_framework import routers

from aids.api.views import AidViewSet, AidAudiences, AidTypes, AidSteps


router = routers.SimpleRouter()
router.register(r'audiences', AidAudiences, basename='aid-audiences')
router.register(r'types', AidTypes, basename='aid-types')
router.register(r'steps', AidSteps, basename='aid-steps')
router.register('', AidViewSet, basename='aids')


urlpatterns = router.urls
