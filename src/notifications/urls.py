from django.urls import path

from notifications.views import NotificationListView, NotificationDeleteView

urlpatterns = [
    path(
        "mes-notifications/",
        NotificationListView.as_view(),
        name="notification_list_view",
    ),
    path(
        "<int:pk>/suppression/",
        NotificationDeleteView.as_view(),
        name="notification_delete_view",
    ),
]
