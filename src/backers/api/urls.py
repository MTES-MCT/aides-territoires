from rest_framework import routers

from backers.api.views import BackerViewSet


router = routers.SimpleRouter()
router.register('', BackerViewSet, base_name='backers')


urlpatterns = router.urls
