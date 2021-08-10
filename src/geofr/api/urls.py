from rest_framework import routers

from geofr.api.views import PerimeterViewSet, PerimeterScales


router = routers.SimpleRouter()
router.register(r'scales', PerimeterScales, basename='perimeter-scales')
router.register('', PerimeterViewSet, basename='perimeters')


urlpatterns = router.urls
