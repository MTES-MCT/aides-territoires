from rest_framework import routers

from projects.api.views import ProjectViewSet


router = routers.SimpleRouter()
router.register('', ProjectViewSet, basename='projects')


urlpatterns = router.urls
