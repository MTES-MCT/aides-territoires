from django.urls import path
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views

from accounts.views import (LoginRequestView, LoginSentView, LoginView,
                            LoginResultView, RegisterView, RegisterSuccessView,
                            ContributorProfileView)


urlpatterns = [
    path(_('register/'), RegisterView.as_view(), name='register'),
    path(_('register-success/'), RegisterSuccessView.as_view(),
         name='register_success'),
    path(_('logout/'), auth_views.LogoutView.as_view(), name='logout'),
    path(_('login-request/'), LoginRequestView.as_view(),
         name='login_request'),
    path(_('login-sent/'), LoginSentView.as_view(), name='login_sent'),
    path(_('login/<uidb64>/<token>/'), LoginView.as_view(), name='login'),
    path(_('login-result/'), LoginResultView.as_view(), name='login_result'),
    path(_('contributor-profile/'), ContributorProfileView.as_view(),
         name='contributor_profile')
]
