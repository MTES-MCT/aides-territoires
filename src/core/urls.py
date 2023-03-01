from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic.base import TemplateView

from rest_framework import routers
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerSplitView,
)

from core.utils import RedirectAidDetailView
from core.otp import OTPAdminSite
from aids.sitemaps import AidSitemap
from data.sitemaps import DataSitemap
from home.sitemaps import HomeSitemap
from pages.sitemaps import PageSitemap
from search.sitemaps import SearchSitemap

router = routers.DefaultRouter()


# Admin
admin.site.site_header = (
    "Administration d'Aides-territoires"  # default: "Django Administration"  # noqa
)
admin.site.index_title = "Accueil"  # default: "Site administration"  # noqa
admin.site.site_title = (
    "Administration d'Aides-territoires"  # default: "Django site admin"  # noqa
)

# Add One Time Password two-factor authentication for the admin site
if settings.ADMIN_OTP_ENABLED:
    admin.site.__class__ = OTPAdminSite


api_patterns = [
    path("", include(router.urls)),
    # This is the public aid list export api
    path("aids/", include("aids.api.urls")),
    # Other public endpoints (also used for autocomplete widgets)
    path("perimeters/", include("geofr.api.urls")),
    path("backers/", include("backers.api.urls")),
    path("programs/", include("programs.api.urls")),
    path("themes/", include("categories.api.urls")),
    path("synonymlists/", include("keywords.api.urls")),
    # Internal api routes
    path("eligibility/", include("eligibility.api.urls")),
    path("stats/", include("stats.api.urls")),
    # Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerSplitView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

sitemaps = {
    "home": HomeSitemap,
    "aids": AidSitemap,
    "pages": PageSitemap,
    "data": DataSitemap,
    "search": SearchSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("comptes/", include("accounts.urls")),
    path("aids/<slug:slug>/", RedirectAidDetailView.as_view()),
    path("aides/", include("aids.urls")),
    path("partenaires/", include("backers.urls")),
    path("blog/", include("blog.urls")),
    path("cartographie/", include("geofr.urls")),
    path("programmes/", include("programs.urls")),
    path("stats/", include("stats.urls")),
    path("alertes/", include("alerts.urls")),
    path("notifications/", include("notifications.urls")),
    path("data/", include("data.urls")),
    path("recherche/", include("search.urls")),
    path("upload/", include("upload.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap_xml"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("admin_tools/", include("admin_tools.urls")),
    path("projets/", include("projects.urls")),
    path("organizations/", include("organizations.urls")),
    # Api related routes
    path("api/", include(api_patterns)),
    # Static pages are at the url root.
    # Leave this at the bottom to prevent an admin to accidently
    # override an existing url.
    path("", include("pages.urls")),
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [
        path(r"__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG and settings.ENABLE_DJANGO_STATIC_SERVE:
    urlpatterns = (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
    )
