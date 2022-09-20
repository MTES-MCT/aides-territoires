from django.urls import path
from pages.views import PageView


urlpatterns = [
    path("<path:url>/", PageView.as_view(), name="page_view"),
]
