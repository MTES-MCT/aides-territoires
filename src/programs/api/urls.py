from rest_framework import routers

from programs.api.views import ProgramViewSet


router = routers.SimpleRouter()
router.register('', ProgramViewSet, basename='programs')


urlpatterns = router.urls
