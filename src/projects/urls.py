from django.urls import path

from projects.views import (ProjectCreateView, ProjectListView,
                            ProjectDetailView, ProjectDeleteView,
                            ProjectUpdateView)


urlpatterns = [
    path('créer/', ProjectCreateView.as_view(),
         name='project_create_view'),
    path('vos-projets/', ProjectListView.as_view(),
         name='project_list_view'),
    path('<int:pk>-<slug:slug>/', ProjectDetailView.as_view(), name='project_detail_view'),
    path('supprimer/<int:pk>/', ProjectDeleteView.as_view(), name='project_delete_view'),
    path('editer/<int:pk>-<slug:slug>/', ProjectUpdateView.as_view(), name='project_update_view'),
]
