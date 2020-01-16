from django.urls import path, include
from django.utils.translation import ugettext_lazy as _

from alerts.views import AlertCreate, AlertDelete

urlpatterns = [
    path(_('create/'), AlertCreate.as_view(), name='alert_create_view'),
    path('<int:pk>/', include([
        path(_('delete/'), AlertDelete.as_view(),
             name='alert_delete_view'),
    ]))
]
