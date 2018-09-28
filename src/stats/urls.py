from django.urls import path

from stats.views import StatsView

urlpatterns = [
    path('', StatsView.as_view(), name='stats_view'),
]
