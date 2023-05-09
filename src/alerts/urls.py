from django.urls import path, include

from alerts.views import (
    AlertCreate,
    AlertDelete,
    AlertValidate,
    AlertListView,
    AlertDeleteFromAccountView,
)

urlpatterns = [
    path("creer/", AlertCreate.as_view(), name="alert_create_view"),
    path(
        "<slug:token>/",
        include(
            [
                path(
                    "validation/", AlertValidate.as_view(), name="alert_validate_view"
                ),
                path("supprimer/", AlertDelete.as_view(), name="alert_delete_view"),
            ]
        ),
    ),
    path("vos-alertes/", AlertListView.as_view(), name="alert_list_view"),
    path(
        "suppression-depuis-le-compte",
        AlertDeleteFromAccountView.as_view(),
        name="alert_delete_from_account_view",
    ),
]
