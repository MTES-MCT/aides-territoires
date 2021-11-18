from django.urls import path

from organizations.views import OrganizationCreateView, OrganizationUpdateView

urlpatterns = [
    path('création/', OrganizationCreateView.as_view(), name='organization_create_view'),
    path('<int:pk>/mise-à-jour/', OrganizationUpdateView.as_view(),
         name='organization_update_view'),
]
