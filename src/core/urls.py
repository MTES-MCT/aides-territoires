from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, reverse_lazy
from django.utils.translation import gettext_lazy as _

from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core.utils import RedirectAidDetailView
from aids.sitemaps import AidSitemap
from data.sitemaps import DataSitemap
from home.sitemaps import HomeSitemap
from pages.sitemaps import PageSitemap
from search.sitemaps import SearchSitemap


router = routers.DefaultRouter()


# Admin
admin.site.site_header = "Administration d'Aides-territoires"  # default: "Django Administration"  # noqa
admin.site.index_title = 'Accueil'                             # default: "Site administration"  # noqa
admin.site.site_title = "Administration d'Aides-territoires"   # default: "Django site admin"  # noqa


# API
schema_view = get_schema_view(
    openapi.Info(
        title='Aides-territoires API',
        default_version=f'v{settings.CURRENT_API_VERSION}',
        # description='',
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
    path('projects/', include('projects.api.urls')),
    path('eligibility/', include('eligibility.api.urls')),
    path('stats/', include('stats.api.urls')),
    # path('tags/', include('tags.api.urls')),
]

sitemaps = {
    'home': HomeSitemap,
    'aids': AidSitemap,
    'pages': PageSitemap,
    'data': DataSitemap,
    'search': SearchSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('home.urls')),
    path(_('accounts/'), include('accounts.urls')),
    path('aids/<slug:slug>/', RedirectAidDetailView.as_view()),
    path('aides/', include('aids.urls')),
    path(_('backers/'), include('backers.urls')),
    path(_('blog/'), include('blog.urls')),
    path(_('programs/'), include('programs.urls')),
    path(_('projects/'), include('projects.urls')),
    path(_('integration/'), include('integration.urls')),
    path(_('stats/'), include('stats.urls')),
    path(_('alerts/'), include('alerts.urls')),
    path(_('tags/'), include('tags.urls')),
    path(_('data/'), include('data.urls')),
    path(_('search/'), include('search.urls')),
    path(_('upload/'), include('upload.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

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

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG and settings.ENABLE_DJANGO_STATIC_SERVE:
    urlpatterns = static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
