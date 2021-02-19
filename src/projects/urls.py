from django.urls import path
from django.utils.translation import gettext_lazy as _

from projects.views import ProjectSuggest

urlpatterns = [
    path(_('suggestproject/'), ProjectSuggest.as_view(),
         name='project_suggest_view'),
]
