from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from search.views import GeneralSearch
from minisites.views import SiteHome


urlpatterns = [
    path('trouver-des-aides/', GeneralSearch.as_view(), name='general_search'),
    path('<slug:search_slug>/', SiteHome.as_view(
        template_name='search/search_page.html'), name='search_page'),
]
