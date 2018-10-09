from django.urls import path

from bundles.views import BundleListView

urlpatterns = [
    path('', BundleListView.as_view(), name='bundle_list_view'),
]
