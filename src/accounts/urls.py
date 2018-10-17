from django.urls import path
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views

from accounts.views import LoginView


urlpatterns = [
    path(_('login/'), LoginView.as_view(), name='login'),
    path(_('logout/'), auth_views.LogoutView.as_view(), name='logout'),
]
