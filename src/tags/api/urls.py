from rest_framework import routers

from tags.api.views import TagViewSet


router = routers.SimpleRouter()
router.register('', TagViewSet, basename='tags')


urlpatterns = router.urls
