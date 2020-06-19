from django.urls import path, include
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.static import static

from minisites.views import Home, Search


urlpatterns = [
    path('', Home.as_view(),  name='home'),
    path(_('search/'), Search.as_view(),
         name='advanced_search_view'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns = static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
