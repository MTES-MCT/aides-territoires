from django.urls import path

from projects.views import (ProjectCreateView, ProjectListView,
                            ProjectDetailView, ProjectDeleteView)


urlpatterns = [
    path('créer/', ProjectCreateView.as_view(),
         name='project_create_view'),
    path('vos-projets/', ProjectListView.as_view(),
         name='project_list_view'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project_detail_view'),
    path('<slug:slug>/supprimer/', ProjectDeleteView.as_view(), name='project_delete_view'),
]
