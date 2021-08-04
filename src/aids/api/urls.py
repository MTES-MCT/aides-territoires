from rest_framework import routers

from aids.api.views import AidViewSet, AidAudiences


router = routers.SimpleRouter()
router.register(r'audiences', AidAudiences, basename='aid-audiences')
router.register('', AidViewSet, basename='aids')


urlpatterns = router.urls
