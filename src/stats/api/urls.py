from rest_framework import routers

from stats.api.views import AidMatchProjectEventViewSet


router = routers.SimpleRouter()
router.register(r'aid-match-project-events', AidMatchProjectEventViewSet,
                basename='aid-match-project-events')


urlpatterns = router.urls
