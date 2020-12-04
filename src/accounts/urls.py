from django.urls import path
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views

from accounts.forms import LoginForm
from accounts.views import (PasswordResetView, PasswordResetSentView,
                            TokenLoginView, RegisterView, RegisterSuccessView,
                            ContributorProfileView)

urlpatterns = [
    path(_('register/'), RegisterView.as_view(), name='register'),
    path(_('register-success/'), RegisterSuccessView.as_view(),
         name='register_success'),

    path(_('login/'), auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True,
    ), name='login'),
    path(_('login/<uidb64>/<token>/'), TokenLoginView.as_view(),
         name='token_login'),

    path(_('password-reset/'), PasswordResetView.as_view(),
         name='password_reset'),
    path(_('password-reset-sent/'), PasswordResetSentView.as_view(),
         name='password_reset_sent'),

    path(_('contributor-profile/'), ContributorProfileView.as_view(),
         name='contributor_profile'),

    path(_('logout/'), auth_views.LogoutView.as_view(), name='logout'),
]
