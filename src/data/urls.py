from django.urls import path

from data.views import DataDocView

urlpatterns = [
    path("", DataDocView.as_view(), name="data_doc"),
]
