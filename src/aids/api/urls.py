from rest_framework import routers

from aids.api.views import AidViewSet, AllAidViewSet


router = routers.SimpleRouter()
router.register(r'all', AllAidViewSet, basename='aids-all')
router.register('', AidViewSet, basename='aids')


urlpatterns = router.urls
