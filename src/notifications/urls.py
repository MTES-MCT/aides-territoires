from django.urls import path

from notifications.views import (
    NotificationDeleteAllView,
    NotificationListView,
    NotificationDeleteView,
    NotificationMarkAllReadView,
    NotificationSettingsView,
)

urlpatterns = [
    path(
        "",
        NotificationListView.as_view(),
        name="notification_list_view",
    ),
    path(
        "préférences/",
        NotificationSettingsView.as_view(),
        name="notification_settings_view",
    ),
    path(
        "tout-marquer-comme-vu/",
        NotificationMarkAllReadView.as_view(),
        name="notification_mark_all_read_view",
    ),
    path(
        "tout-supprimer/",
        NotificationDeleteAllView.as_view(),
        name="notification_delete_all_view",
    ),
    path(
        "<int:pk>/suppression/",
        NotificationDeleteView.as_view(),
        name="notification_delete_view",
    ),
]
