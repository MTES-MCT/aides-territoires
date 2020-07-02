from rest_framework import routers
from django.urls import path, include
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.static import static

from minisites.views import Home, Search, Aid, Alert, LegalMentions


router = routers.DefaultRouter()

api_patterns = [
    path('', include(router.urls)),
    path('perimeters/', include('geofr.api.urls')),
    path('backers/', include('backers.api.urls')),
]

urlpatterns = [
    path('', Home.as_view(),  name='home'),
    path('', Home.as_view(),  name='search_view'),
    path(_('search/'), Search.as_view(), name='advanced_search_view'),
    path('<slug:slug>/', include([
        path('', Aid.as_view(), name='aid_detail_view')])),
    path(_('alert/'), Alert.as_view(), name='alert_create_view'),
    path(_('legal-mentions/'), LegalMentions.as_view(), name='legal_mentions'),


    # Api related routes
    path('api/', include(api_patterns)),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns = static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
