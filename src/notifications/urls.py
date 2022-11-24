from django.urls import path

from notifications.views import (
    NotificationListView,
)

urlpatterns = [
    path(
        "mes-notifications/",
        NotificationListView.as_view(),
        name="notification_list_view",
    ),
]
