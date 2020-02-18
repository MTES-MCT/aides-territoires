from django.urls import path
from django.utils.translation import ugettext_lazy as _

from search.views import (AudianceSearch, PerimeterSearch, ThemeSearch,
                          CategorySearch)


urlpatterns = [
    path(_('audiance/'), AudianceSearch.as_view(),
         name='search_step_audiance'),
    path(_('perimeter/'), PerimeterSearch.as_view(),
         name='search_step_perimeter'),
    path(_('theme/'), ThemeSearch.as_view(), name='search_step_theme'),
    path(_('category/'), CategorySearch.as_view(),
         name='search_step_category'),
]
