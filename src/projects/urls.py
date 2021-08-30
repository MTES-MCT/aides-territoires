from django.urls import path

from projects.views import ProjectCreateView, ProjectListView, ProjectMatchAidView


urlpatterns = [
    path('création-projet/', ProjectCreateView.as_view(),
         name='project_create_view'),
    path('aides-projets/<slug:slug>/', ProjectMatchAidView.as_view(),
         name='project_match_aid_view'),
    path('vos-projets/', ProjectListView.as_view(),
         name='project_list_view'),
]