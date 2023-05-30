from django.urls import path
from backers.views import (
    BackerDetailView,
    BackersExclusionListView,
    ToggleBackerExcludeView,
)


urlpatterns = [
    path("<int:pk>/", BackerDetailView.as_view(), name="backer_detail_view"),
    path("<int:pk>-<str>/", BackerDetailView.as_view(), name="backer_detail_view"),
    path(
        "masquer/",
        BackersExclusionListView.as_view(),
        name="backers_exclusion_list",
    ),
    path(
        "masquer/<int:pk>/",
        ToggleBackerExcludeView.as_view(),
        name="toggle_backer_exclude_view",
    ),
]
