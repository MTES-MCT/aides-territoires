from django.urls import path

from organizations.views import (
    OrganizationCreateView,
    OrganizationUpdateView,
    AddProjectToFavoriteView,
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
]
