from django.urls import path

from stats.views import StatsView, DashboardView, UsersStatsView

urlpatterns = [
    path('', StatsView.as_view(), name='stats_view'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_view'),
    path('utilisateurs-stats/', UsersStatsView.as_view(), name='users_stats'),
]
