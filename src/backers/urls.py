from unicodedata import name
from django.urls import path
from backers.views import (
    BackerDepartementProgramsView,
    BackerDetailView,
    BackerMapView,
    BackerDepartementView,
    BackerDepartementBackersView,
)


urlpatterns = [
    path("<int:pk>/", BackerDetailView.as_view(), name="backer_detail_view"),
    path("<int:pk>-<str>/", BackerDetailView.as_view(), name="backer_detail_view"),
    path("cartographie/", BackerMapView.as_view(), name="backer_map_view"),
    path(
        "cartographie/<int:pk>-<str:slug>/",
        BackerDepartementView.as_view(),
        name="backer_departement_view",
    ),
    path(
        "cartographie/<int:pk>-<str:slug>/porteurs/",
        BackerDepartementBackersView.as_view(),
        name="backer_departement_backers_view",
    ),
    path(
        "cartographie/<int:pk>-<str:slug>/programmes/",
        BackerDepartementProgramsView.as_view(),
        name="backer_departement_programs_view",
    ),
]
