from rest_framework import routers

from aids.api.views import AidViewSet


router = routers.SimpleRouter()
router.register('', AidViewSet, base_name='aids')


urlpatterns = router.urls
