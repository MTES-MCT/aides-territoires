from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views

from accounts.forms import LoginForm
from accounts.views import (PasswordResetView, PasswordResetSentView,
                            TokenLoginView, RegisterView, RegisterSuccessView,
                            ContributorProfileView, UserDashboardView,
                            UserApiTokenView, UnSubscribeNewsletter,
                            InviteCollaborator, CollaboratorsList, CompleteProfileView)


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

    path('monprofil/', ContributorProfileView.as_view(),
         name='contributor_profile'),
    path('completer-votre-profil/', CompleteProfileView.as_view(),
         name='complete_profile'),

    path('moncompte/', UserDashboardView.as_view(),
         name='user_dashboard'),
    path(_('api-token/'), UserApiTokenView.as_view(),
         name='api_token'),
    path(_('logout/'), auth_views.LogoutView.as_view(), name='logout'),

    path('desinscription-newsletter/', UnSubscribeNewsletter.as_view(),
         name='unsubscribe_nawsletter'),
    path('inviter-collaborateur/', InviteCollaborator.as_view(),
         name='invite_collaborator'),
    path('collaborateurs/', CollaboratorsList.as_view(),
         name='collaborators'),
]
