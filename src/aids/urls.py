from django.urls import path
from django.utils.translation import ugettext_lazy as _

from aids.views import SearchView, ResultsView, AidDetailView, AidCreateView

urlpatterns = [
    path('', SearchView.as_view(), name='search_view'),
    path(_('results/'), ResultsView.as_view(), name='results_view'),
    path(_('add/'), AidCreateView.as_view(), name='aid_create_view'),
    path('<slug:slug>/', AidDetailView.as_view(), name='aid_detail_view'),
]
