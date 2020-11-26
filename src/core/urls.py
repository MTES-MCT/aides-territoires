from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import routers, permissions


router = routers.DefaultRouter()


schema_view = get_schema_view(
   openapi.Info(
      title=_('Aides-Territoires API'),
      default_version='v1',
      description=_('API Aide'),
      terms_of_service=reverse_lazy('legal_mentions'),
      contact=openapi.Contact(email='tech@aides-territoires.beta.gouv.fr'),
      license=openapi.License(name="« Licence Ouverte v2.0 » d'Etalab"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

api_patterns = [

    path('', include(router.urls)),

    # This is the public aid list export api
    path('aids/', include('aids.api.urls')),

    # Those are internal api routes (for autocomplete widgets mostly)
    path('perimeters/', include('geofr.api.urls')),
    path('backers/', include('backers.api.urls')),
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
    path(_('alerts/'), include('alerts.urls')),
    path(_('tags/'), include('tags.urls')),
    path(_('data/'), include('data.urls')),
    path(_('search/'), include('search.urls')),
    path(_('upload/'), include('upload.urls')),

    # Api related routes
    path('api/', include(api_patterns)),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    # Static pages are at the url root.
    # Leave this at the bottom to prevent an admin to accidently
    # override an existing url.
    path('', include('pages.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns = static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
