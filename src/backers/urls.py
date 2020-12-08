from django.urls import path
from backers.views import BackerDetailView


urlpatterns = [
    path(
        '<int:pk>-<slug:slug>/', BackerDetailView.as_view(),
        name='backer_detail_view'),
]
