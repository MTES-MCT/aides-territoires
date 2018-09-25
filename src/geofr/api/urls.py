from rest_framework import routers

from geofr.api.views import PerimeterViewSet


router = routers.SimpleRouter()
router.register('', PerimeterViewSet, base_name='perimeters')


urlpatterns = router.urls
