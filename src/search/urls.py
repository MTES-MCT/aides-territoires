from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from search.views import (AudienceSearch, PerimeterSearch, ThemeSearch,
                          CategorySearch)
from minisites.views import SiteHome


urlpatterns = [
    path(_('form/'), include([
        path(_('audience/'), AudienceSearch.as_view(),
             name='search_step_audience'),
        path(_('perimeter/'), PerimeterSearch.as_view(),
             name='search_step_perimeter'),
        path(_('theme/'), ThemeSearch.as_view(), name='search_step_theme'),
        path(_('category/'), CategorySearch.as_view(),
             name='search_step_category'),
    ])),
    path('<slug:search_slug>/', SiteHome.as_view(
        template_name='search/search_page.html'), name='search_page'),
]
