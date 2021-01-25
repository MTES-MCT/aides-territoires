from django.urls import path
from django.utils.translation import gettext_lazy as _

from bundles.views import BundleListView, BundleCreateView

urlpatterns = [
    path('', BundleListView.as_view(), name='bundle_list_view'),
    path(_('create/'), BundleCreateView.as_view(), name='bundle_create_view'),
    path('<slug>', BundleListView.as_view(), name='bundle_list_view'),
]
