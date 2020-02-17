from django.urls import path
from django.utils.translation import ugettext_lazy as _

from search.views import AudianceSearch, PerimeterSearch


urlpatterns = [
    path(_('audiance/'), AudianceSearch.as_view(),
         name='search_step_audiance'),
    path(_('perimeter/'), PerimeterSearch.as_view(),
         name='search_step_perimeter'),
]
