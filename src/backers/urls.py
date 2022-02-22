from unicodedata import name
from django.urls import path
from backers.views import BackerDetailView, BackerMapView, BackerDepartementView


urlpatterns = [
    path(
        '<int:pk>/', BackerDetailView.as_view(),
        name='backer_detail_view'),
    path(
        '<int:pk>-<str>/', BackerDetailView.as_view(),
        name='backer_detail_view'),
    path(
        'cartographie/', BackerMapView.as_view(),
        name='backer_map_view'),
    path(
        'cartographie/<str:code>/', BackerDepartementView.as_view(),
        name='backer_departement_view')
]
