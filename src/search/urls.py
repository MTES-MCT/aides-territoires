from django.urls import path

from minisites.views import SiteHome, SiteStats


urlpatterns = [
    path(
        "<slug:search_slug>/",
        SiteHome.as_view(template_name="search/search_page.html"),
        name="search_page",
    ),
    path(
        "<slug:search_slug>/",
        SiteHome.as_view(template_name="search/search_page.html"),
        name="search_minisite_view",
    ),
    path(
        "<slug:search_slug>/stats/",
        SiteStats.as_view(template_name="search/search_stats.html"),
        name="search_stats_view",
    ),
]
