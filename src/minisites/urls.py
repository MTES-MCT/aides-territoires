from django.urls import path

from minisites.views import SearchView


urlpatterns = [
    path('', SearchView.as_view(), name='minisite_search'),
]
