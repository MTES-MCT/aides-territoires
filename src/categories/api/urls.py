from rest_framework import routers

from categories.api.views import ThemeViewSet


router = routers.SimpleRouter()
router.register('', ThemeViewSet, basename='themes')


urlpatterns = router.urls
