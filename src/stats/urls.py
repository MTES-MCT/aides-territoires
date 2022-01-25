from django.urls import path

from stats.views import StatsView, DashboardView, UsersStatsView, ProjectsStatsView

urlpatterns = [
    path('', StatsView.as_view(), name='stats_view'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_view'),
    path('stats-utilisateurs/', UsersStatsView.as_view(), name='users_stats'),
    path('stats-projets/', ProjectsStatsView.as_view(), name='projects_stats'),
]
