from django.urls import path

from projects.views import (
    ProjectCreateView,
    ProjectExportView,
    ProjectListView,
    PublicProjectListView,
    PublicFinishedProjectResultsView,
    PublicFinishedProjectHomeView,
    FavoriteProjectListView,
    ProjectDetailView,
    PublicProjectDetailView,
    FavoriteProjectDetailView,
    ProjectDeleteView,
    ProjectUpdateView,
)


urlpatterns = [
    path("créer/", ProjectCreateView.as_view(), name="project_create_view"),
    path("vos-projets/", ProjectListView.as_view(), name="project_list_view"),
    path(
        "projets-publics/",
        PublicProjectListView.as_view(),
        name="public_project_list_view",
    ),
    path(
        "projets-subventionnés/résultats/",
        PublicFinishedProjectResultsView.as_view(),
        name="public_finished_project_results_view",
    ),
    path(
        "projets-subventionnés/",
        PublicFinishedProjectHomeView.as_view(),
        name="public_finished_project_home_view",
    ),
    path(
        "projets-favoris/",
        FavoriteProjectListView.as_view(),
        name="favorite_project_list_view",
    ),
    path(
        "<int:pk>-<slug:slug>/", ProjectDetailView.as_view(), name="project_detail_view"
    ),
    path(
        "projets-publics/<int:pk>-<slug:slug>/",
        PublicProjectDetailView.as_view(),
        name="public_project_detail_view",
    ),
    path(
        "projets-favoris/<int:pk>-<slug:slug>/",
        FavoriteProjectDetailView.as_view(),
        name="favorite_project_detail_view",
    ),
    path(
        "supprimer/<int:pk>/", ProjectDeleteView.as_view(), name="project_delete_view"
    ),
    path(
        "editer/<int:pk>-<slug:slug>/",
        ProjectUpdateView.as_view(),
        name="project_update_view",
    ),
    path("exporter/<int:pk>/", ProjectExportView.as_view(), name="project_export_view"),
]
