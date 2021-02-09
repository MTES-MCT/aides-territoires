from rest_framework import routers
from django.urls import path, include
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.views.generic import View

from minisites.views import (SiteHome, SiteSearch, SiteAid, SiteAlert,
                             SiteBackers, SiteStats, SiteProgram,
                             SiteLegalMentions, Error)


# This set of url patterns is completely independant from all other urls.
# The `normal` core url patterns is set in `core.settings` to `core.urls`
# This is a custom set of url patterns, set in `minisites.settings`.


router = routers.DefaultRouter()

api_patterns = [
    path('', include(router.urls)),
    path('perimeters/', include('geofr.api.urls')),
    path('backers/', include('backers.api.urls')),
]

urlpatterns = [

    # We give two names to the same view, because with minisites, the search
    # form is also the home page.
    path('', SiteHome.as_view(),  name='home'),
    path('', SiteHome.as_view(),  name='search_view'),

    # This is the full search form
    path(_('search/'), SiteSearch.as_view(), name='advanced_search_view'),

    # Minisite users must be able to create alerts
    path(_('alerts/'), include([
        path('', SiteAlert.as_view(), name='alert_create_view'),

        # We need to define this url so django can resolve it and generate a
        # token validation email. However, when the user clicks this link,
        # they will be sent to the regular site
        path(_('<slug:token>/validate/'), View.as_view(),
             name='alert_validate_view'),
    ])),

    path(_('stats/'), SiteStats.as_view(), name='stats_view'),

    path(_('programs/<slug:slug>/'), SiteProgram.as_view(),
         name='program_detail'),

    path(_('backers/<int:pk>/'), SiteBackers.as_view(),
         name='backer_detail_view'),
    path(_('backers/<int:pk>-<str>/'), SiteBackers.as_view(),
         name='backer_detail_view'),

    path(_('legal-mentions/'), SiteLegalMentions.as_view(),
         name='legal_mentions'),

    # Api related routes
    path('api/', include(api_patterns)),

    # The aid detail view
    path('<slug:slug>/', include([
        path('', SiteAid.as_view(), name='aid_detail_view')])),
]

handler400 = Error.as_view(template_name='minisites/400.html', status_code=400)
handler403 = Error.as_view(template_name='minisites/403.html', status_code=403)
handler404 = Error.as_view(template_name='minisites/404.html', status_code=404)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns = static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
