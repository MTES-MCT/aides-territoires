from django.urls import path

from stats.views import (
    StatsView,
    DashboardView,
    UsersStatsView,
    CartoStatsView,
    ProjectsStatsView,
    OrganizationsStatsView,
)

urlpatterns = [
    path("", StatsView.as_view(), name="stats_view"),
    path("dashboard/", DashboardView.as_view(), name="dashboard_view"),
    path("stats-utilisateurs/", UsersStatsView.as_view(), name="users_stats"),
    path("stats-cartographie/", CartoStatsView.as_view(), name="carto_stats"),
    path("stats-projets/", ProjectsStatsView.as_view(), name="projects_stats"),
    path(
        "stats-structures/",
        OrganizationsStatsView.as_view(),
        name="organizations_stats",
    ),
]
