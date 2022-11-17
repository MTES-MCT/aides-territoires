from django.urls import path

from organizations.views import (
    OrganizationCreateView,
    OrganizationUpdateView,
    AddProjectToFavoriteView,
    RemoveProjectFromFavoriteView,
)

urlpatterns = [
    path(
        "création/", OrganizationCreateView.as_view(), name="organization_create_view"
    ),
    path(
        "<int:pk>/mise-à-jour/",
        OrganizationUpdateView.as_view(),
        name="organization_update_view",
    ),
    path(
        "<int:pk>/ajout-aux-projets-favoris/",
        AddProjectToFavoriteView.as_view(),
        name="add_project_to_favorite_view",
    ),
    path(
        "<int:pk>/retrait-des-projets-favoris/",
        RemoveProjectFromFavoriteView.as_view(),
        name="remove_project_from_favorite_view",
    ),
]
