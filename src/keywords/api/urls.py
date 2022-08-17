from rest_framework import routers

from keywords.api.views import SynonymListViewSet


router = routers.SimpleRouter()
router.register('', SynonymListViewSet, basename='synonymLists')


urlpatterns = router.urls
