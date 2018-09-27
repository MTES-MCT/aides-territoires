from django.urls import path

from integration.views import GuyaneGouvView, SommeView

urlpatterns = [
    path('guyane/', GuyaneGouvView.as_view(), name='guyane_gouv_view'),
    path('somme/', SommeView.as_view(), name='somme_view'),
]
