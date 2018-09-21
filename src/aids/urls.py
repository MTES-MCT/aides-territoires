from django.urls import path

from aids.views import SearchView, AidCreateView

urlpatterns = [
    path('', SearchView.as_view(), name='search_view'),
    path('create', AidCreateView.as_view(), name='aid_create_view'),
]
