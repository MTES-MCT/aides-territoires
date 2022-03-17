from unicodedata import name
from django.urls import path
from backers.views import BackerDetailView


urlpatterns = [
    path("<int:pk>/", BackerDetailView.as_view(), name="backer_detail_view"),
    path("<int:pk>-<str>/", BackerDetailView.as_view(), name="backer_detail_view"),
]
