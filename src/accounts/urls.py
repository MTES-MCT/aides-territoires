from django.urls import path
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(_('logout/'), auth_views.LogoutView.as_view(), name='logout'),
]
