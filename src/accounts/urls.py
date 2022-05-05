from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.forms import LoginForm
from accounts.views import (
    PasswordResetView,
    PasswordResetSentView,
    PasswordResetConfirmView,
    LoginView,
    TokenLoginView,
    RegisterView,
    RegisterSuccessView,
    ContributorProfileView,
    UserDashboardView,
    UserApiTokenView,
    UnSubscribeNewsletter,
    SubscribeNewsletter,
    InviteCollaborator,
    CollaboratorsList,
    CompleteProfileView,
    HistoryLoginList,
    DeleteHistoryLoginView,
)


urlpatterns = [
    path("inscription/", RegisterView.as_view(), name="register"),
    path("inscription-succès/", RegisterSuccessView.as_view(), name="register_success"),
    path(
        "connexion/",
        LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("connexion/<uidb64>/<token>/", TokenLoginView.as_view(), name="token_login"),
    path(
        "mot-de-passe-confirmation/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("nouveau-mot-de-passe/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "mot-de-passe-envoyé/",
        PasswordResetSentView.as_view(),
        name="password_reset_sent",
    ),
    path("monprofil/", ContributorProfileView.as_view(), name="contributor_profile"),
    path(
        "completer-votre-profil/",
        CompleteProfileView.as_view(),
        name="complete_profile",
    ),
    path("moncompte/", UserDashboardView.as_view(), name="user_dashboard"),
    path("api-token/", UserApiTokenView.as_view(), name="api_token"),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "desinscription-newsletter/",
        UnSubscribeNewsletter.as_view(),
        name="unsubscribe_newsletter",
    ),
    path(
        "inscription-newsletter/",
        SubscribeNewsletter.as_view(),
        name="subscribe_newsletter",
    ),
    path(
        "inviter-collaborateur/",
        InviteCollaborator.as_view(),
        name="invite_collaborator",
    ),
    path("collaborateurs/", CollaboratorsList.as_view(), name="collaborators"),
    path("journal-de-connexion/", HistoryLoginList.as_view(), name="history_login"),
    path(
        "suppression-journal-de-connexion/",
        DeleteHistoryLoginView.as_view(),
        name="delete_history_login",
    ),
]
