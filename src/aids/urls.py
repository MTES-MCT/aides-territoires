from django.urls import path

from aids.views import SearchView

urlpatterns = [
    path('', SearchView.as_view(), name='search_view'),
]
