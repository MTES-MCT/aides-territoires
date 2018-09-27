from django.urls import path

from integration.views import GuyaneGouvView

urlpatterns = [
    path('guyane/', GuyaneGouvView.as_view(), name='guyane_gouv_view'),
]
