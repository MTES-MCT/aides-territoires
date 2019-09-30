from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


router = routers.DefaultRouter()

api_patterns = [
    path('', include(router.urls)),
    path('perimeters/', include('geofr.api.urls')),
    path('backers/', include('backers.api.urls')),
    path('aids/', include('aids.api.urls')),
    path('tags/', include('tags.api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('home.urls')),
    path(_('accounts/'), include('accounts.urls')),
    path(_('aids/'), include('aids.urls')),
    path(_('programs/'), include('programs.urls')),
    path(_('integration/'), include('integration.urls')),
    path(_('stats/'), include('stats.urls')),
    path(_('bundles/'), include('bundles.urls')),
    path(_('bookmarks/'), include('bookmarks.urls')),
    path(_('tags/'), include('tags.urls')),
    path(_('data/'), include('data.urls')),

    # Api related routes
    path('api/', include(api_patterns)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
