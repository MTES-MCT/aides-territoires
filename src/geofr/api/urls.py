from rest_framework import routers

from geofr.api.views import PerimeterViewSet, PerimeterScalesViewSet


router = routers.SimpleRouter()
router.register(r"scales", PerimeterScalesViewSet, basename="perimeter-scales")
router.register("", PerimeterViewSet, basename="perimeters")


urlpatterns = router.urls
