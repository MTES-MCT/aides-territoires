from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from alerts.views import AlertCreate, AlertDelete, AlertValidate

urlpatterns = [
    path(_('create/'), AlertCreate.as_view(), name='alert_create_view'),
    path('<slug:token>/', include([
        path(_('validate/'), AlertValidate.as_view(),
             name='alert_validate_view'),
        path(_('delete/'), AlertDelete.as_view(),
             name='alert_delete_view'),
    ]))
]
