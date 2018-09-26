from django.urls import path
from django.utils.translation import ugettext_lazy as _

from aids.views import SearchView, AidCreateView

urlpatterns = [
    path('', SearchView.as_view(), name='search_view'),
    path(_('add/'), AidCreateView.as_view(), name='aid_create_view'),
]
