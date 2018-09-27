from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


router = routers.DefaultRouter()

api_patterns = [
    path('', include(router.urls)),
    path('perimeters', include('geofr.api.urls')),
    path('backers', include('backers.api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('home.urls')),
    path(_('aids/'), include('aids.urls')),
    path(_('integration/'), include('integration.urls')),

    # Api related routes
    path('api/', include(api_patterns)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
