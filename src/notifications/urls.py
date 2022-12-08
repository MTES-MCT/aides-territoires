from django.urls import path

from notifications.views import (
    NotificationDetailView,
    NotificationListView,
    NotificationDeleteView,
)

urlpatterns = [
    path(
        "",
        NotificationListView.as_view(),
        name="notification_list_view",
    ),
    path(
        "<int:pk>/",
        NotificationDetailView.as_view(),
        name="notification_detail_view",
    ),
    path(
        "<int:pk>/suppression/",
        NotificationDeleteView.as_view(),
        name="notification_delete_view",
    ),
]
