from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from minisites.views import SearchView


urlpatterns = [
    path('', SearchView.as_view(), name='home'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns = static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
