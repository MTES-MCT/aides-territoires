from django.urls import path
from map.views import (
    DepartmentProgramsView,
    MapView,
    DepartmentView,
    DepartmentBackersView,
)


urlpatterns = [
    path("", MapView.as_view(), name="map_view"),
    path(
        "<int:pk>-<str:slug>/",
        DepartmentView.as_view(),
        name="department_view",
    ),
    path(
        "<int:pk>-<str:slug>/porteurs/",
        DepartmentBackersView.as_view(),
        name="department_backers_view",
    ),
    path(
        "<int:pk>-<str:slug>/programmes/",
        DepartmentProgramsView.as_view(),
        name="department_programs_view",
    ),
]
