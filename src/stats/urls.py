from django.urls import path

from stats.views import (
    StatsView,
    DashboardAcquisitionView,
    DashboardConsultationView,
    DashboardEngagementView,
    DashboardPorteursView,
    UsersStatsView,
    CartoStatsView,
    ProjectsStatsView,
    OrganizationsStatsView,
)

urlpatterns = [
    path("", StatsView.as_view(), name="stats_view"),
    path(
        "dashboard/acquisition/",
        DashboardAcquisitionView.as_view(),
        name="dashboard_acquisition_view",
    ),
    path(
        "dashboard/engagement/",
        DashboardEngagementView.as_view(),
        name="dashboard_engagement_view",
    ),
    path(
        "dashboard/porteurs/",
        DashboardPorteursView.as_view(),
        name="dashboard_porteurs_view",
    ),
    path("dashboard/", DashboardConsultationView.as_view(), name="dashboard_view"),
    path("stats-utilisateurs/", UsersStatsView.as_view(), name="users_stats"),
    path("stats-cartographie/", CartoStatsView.as_view(), name="carto_stats"),
    path("stats-projets/", ProjectsStatsView.as_view(), name="projects_stats"),
    path(
        "stats-structures/",
        OrganizationsStatsView.as_view(),
        name="organizations_stats",
    ),
]
