from django.urls import path
from backers.views import BackerDetailView, BackersBlacklistView


urlpatterns = [
    path("<int:pk>/", BackerDetailView.as_view(), name="backer_detail_view"),
    path("<int:pk>-<str>/", BackerDetailView.as_view(), name="backer_detail_view"),
    path(
        "masquer/",
        BackersBlacklistView.as_view(),
        name="backers_blacklist",
    ),
]
