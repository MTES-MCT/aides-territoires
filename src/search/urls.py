from django.urls import path
from django.utils.translation import ugettext_lazy as _

from search.views import AudianceSearch


urlpatterns = [
    path(_('audiance/'), AudianceSearch.as_view(), name='search_step_audiance'),
]
