from django.urls import path

from organizations.views import OrganizationCreateView

urlpatterns = [
    path('création/', OrganizationCreateView.as_view(), name='organization_create_view'),
]
