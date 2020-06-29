from django.urls import path, include
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.static import static

from minisites.views import Home, Search, Aid, Alert
from geofr.api.urls import router


urlpatterns = [
    path('', Home.as_view(),  name='home'),
    path(_('search/'), Search.as_view(),
         name='advanced_search_view'),
    path('<slug:slug>/', include([
        path('', Aid.as_view(), name='aid_detail_view'),
    ])),
    path(_('alert/'), Alert.as_view(), name='alert_create_view'),
]

urlpatterns += router.urls

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns = static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
