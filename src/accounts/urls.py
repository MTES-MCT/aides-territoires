from django.urls import path
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views

from accounts.views import LoginRequestView, LoginSentView


urlpatterns = [
    path(_('logout/'), auth_views.LogoutView.as_view(), name='logout'),
    path(_('login-request/'), LoginRequestView.as_view(), name='login_request'),
    path(_('login-sent/'), LoginSentView.as_view(), name='login_sent'),
]
