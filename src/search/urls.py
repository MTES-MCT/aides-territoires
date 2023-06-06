from django.urls import path

from minisites.views import SiteHome


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
]
