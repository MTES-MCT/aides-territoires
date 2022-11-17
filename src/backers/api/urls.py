from rest_framework import routers

from backers.api.views import BackerViewSet


router = routers.SimpleRouter()
router.register("", BackerViewSet, basename="backers")


urlpatterns = router.urls
