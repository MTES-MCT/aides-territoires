from rest_framework import routers

from geofr.api.views import (
    PerimeterDataViewSet,
    PerimeterViewSet,
    PerimeterScalesViewSet,
)


router = routers.SimpleRouter()
router.register(r"scales", PerimeterScalesViewSet, basename="perimeter-scales")
router.register(r"data", PerimeterDataViewSet, basename="perimeter-data")
router.register("", PerimeterViewSet, basename="perimeters")

urlpatterns = router.urls
