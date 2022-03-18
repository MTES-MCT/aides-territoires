from django.urls import path, re_path
from geofr.views import (
    DepartmentProgramsView,
    MapView,
    DepartmentView,
    DepartmentBackersView,
)


urlpatterns = [
    path("", MapView.as_view(), name="map_view"),
    re_path(
        r"^(?P<code>[0-9AB]{2,3})-(?P<slug>[\w-]+)/$",
        DepartmentView.as_view(),
        name="department_view",
    ),
    re_path(
        r"^(?P<code>[0-9AB]{2,3})-(?P<slug>[\w-]+)/porteurs/$",
        DepartmentBackersView.as_view(),
        name="department_backers_view",
    ),
    re_path(
        r"^(?P<code>[0-9AB]{2,3})-(?P<slug>[\w-]+)/programmes/$",
        DepartmentProgramsView.as_view(),
        name="department_programs_view",
    ),
]
