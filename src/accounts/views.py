import requests

from django.conf import settings
from django.views.generic import (
    FormView,
    TemplateView,
    CreateView,
    UpdateView,
    View,
    ListView,
)
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login, update_session_auth_hash, views
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.shortcuts import resolve_url

from braces.views import AnonymousRequiredMixin, MessageMixin

from accounts.mixins import (
    ContributorAndProfileCompleteRequiredMixin,
    ContributorRequiredMixin,
    UserLoggedRequiredMixin,
)
from accounts.forms import (
    RegisterForm,
    PasswordResetForm,
    PasswordResetConfirmForm,
    ContributorProfileForm,
    InviteCollaboratorForm,
    CompleteProfileForm,
    JoinOrganizationForm
)
from accounts.tasks import (
    send_connection_email,
    send_invitation_email,
    send_welcome_email,
)
from accounts.models import User, UserLastConnexion
from projects.models import Project
from aids.models import Aid
from organizations.models import Organization
from analytics.utils import track_goal


class RegisterView(AnonymousRequiredMixin, CreateView):
    """Allow users to create new accounts."""

    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("organization_create_view")

    def form_valid(self, form):
        """Send a connection/confirmation link to the user."""
        user_organization_type = self.request.POST.get("organization_type", None)
        user_email = form.cleaned_data["email"]
        user_first_name = form.cleaned_data["first_name"]
        user_last_name = form.cleaned_data["last_name"]
        self.request.session["USER_EMAIL"] = user_email
        self.request.session["USER_ORGANIZATION_TYPE"] = user_organization_type
        self.request.session["USER_NAME"] = user_first_name + " " + user_last_name
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        return context


class RegisterSuccessView(AnonymousRequiredMixin, TemplateView):
    """Display success message after register action."""

    template_name = "accounts/register_success.html"


class PasswordResetView(AnonymousRequiredMixin, FormView):
    """Implement a simple login form using email only."""

    template_name = "accounts/password_reset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("password_reset_sent")

    def form_valid(self, form):
        """Send a login link by email."""
        user_email = form.cleaned_data["username"]
        send_connection_email.delay(user_email, reset_password=True)
        return super().form_valid(form)


class PasswordResetSentView(AnonymousRequiredMixin, TemplateView):
    """Simple success confirmation message."""

    template_name = "accounts/password_reset_sent.html"


class PasswordResetConfirmView(
    ContributorRequiredMixin, SuccessMessageMixin, UpdateView
):
    """Update contributor profile data."""

    template_name = "accounts/password_reset_confirm.html"
    form_class = PasswordResetConfirmForm
    success_message = "Votre mot de passe a bien été mis à jour."

    def get_success_url(self):
        current_url = reverse("user_dashboard")
        next_url = self.request.GET.get("next", current_url)
        return next_url

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        """Make sure the user is not disconnected after password change."""
        res = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return res


class LoginView(views.LoginView, TemplateView):
    next_page = None

    def get_success_url(self):
        UserLastConnexion.objects.create(user=self.request.user)
        return self.get_redirect_url() or self.get_default_redirect_url()

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        return resolve_url(self.next_page or settings.LOGIN_REDIRECT_URL)


class TokenLoginView(AnonymousRequiredMixin, MessageMixin, TemplateView):
    """Check token and authenticates user."""

    template_name = "accounts/login_error.html"

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs["uidb64"]
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (ValueError, User.DoesNotExist):
            user = None

        if user:
            token = kwargs["token"]
            if default_token_generator.check_token(user, token):
                is_first_login = user.last_login is None
                login(self.request, user)
                UserLastConnexion.objects.create(user=self.request.user)

                if is_first_login:
                    msg = "Vous êtes maintenant connecté. Bienvenue ! Pourriez-vous prendre quelques secondes pour mettre à jour votre profil ?"  # noqa
                    track_goal(self.request.session, settings.GOAL_FIRST_LOGIN_ID)
                    send_welcome_email.delay(user.email)
                else:
                    msg = "Vous êtes maintenant connecté. Bienvenue !"

                self.messages.success(msg)
                if self.request.GET.get("next"):
                    redirect_url = reverse(self.request.GET.get("next"))
                else:
                    redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
                return HttpResponseRedirect(redirect_url)

        return super().get(request, *args, **kwargs)


class ContributorProfileView(
    ContributorAndProfileCompleteRequiredMixin, SuccessMessageMixin, UpdateView
):
    """Update contributor profile data."""

    form_class = ContributorProfileForm
    template_name = "accounts/contributor_profile.html"
    success_message = "Votre profil a été mis à jour."

    def get_success_url(self):
        current_url = reverse("contributor_profile")
        next_url = self.request.GET.get("next", current_url)
        return next_url

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        """Make sure the user is not disconnected after password change."""
        res = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return res


class UserDashboardView(ContributorAndProfileCompleteRequiredMixin, TemplateView):
    """User Dashboard"""

    template_name = "accounts/user_dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.beneficiary_organization is not None:
            context["collaborators_number"] = (
                User.objects.filter(
                    beneficiary_organization=self.request.user.beneficiary_organization.pk
                )
                .exclude(pk=self.request.user.pk)
                .count()
            )
            context["projects_number"] = Project.objects.filter(
                organizations=self.request.user.beneficiary_organization.pk
            ).count()
        context["aids_number"] = Aid.objects.filter(author=self.request.user.pk).count()
        if self.request.user.proposed_organization is not None:
            context["join_organization"] = True
        return context


class UserApiTokenView(ContributorAndProfileCompleteRequiredMixin, TemplateView):
    """User can access to his API Token"""

    template_name = "accounts/user_api_token.html"


class SubscribeNewsletter(View):
    def get(self, request):
        """
        Here we want to allow user to unsubscribe to the newsletter.
        """
        SIB_NEWSLETTER_ID = settings.SIB_NEWSLETTER_ID.split(", ")
        SIB_NEWSLETTER_ID = [int(i) for i in SIB_NEWSLETTER_ID]

        user_email = self.request.user.email

        url = "https://api.sendinblue.com/v3/contacts/doubleOptinConfirmation"

        redirection_url = (
            "https://aides-territoires.beta.gouv.fr/inscription-newsletter-succes/"
        )

        payload = {
            "attributes": {"DOUBLE_OPT_IN": "1"},
            "includeListIds": SIB_NEWSLETTER_ID,
            "email": user_email,
            "templateId": settings.SIB_NEWSLETTER_CONFIRM_TEMPLATE_ID,
            "redirectionUrl": redirection_url,
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "api-key": settings.SIB_API_KEY,
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        if response and any((response.status_code == 201, response.status_code == 204)):
            msg = "Votre demande d'inscription à la newsletter a bien été prise en compte."
            "<strong>Afin de finaliser votre inscription il vous reste à cliquer sur le lien"
            "de confirmation présent dans l'e-mail que vous allez recevoir.</strong>"
            messages.success(self.request, msg)
        else:
            msg = "Une erreur s'est produite lors de votre inscription à la newsletter"
            messages.error(self.request, msg)

        redirect_url = reverse("alert_list_view")
        return HttpResponseRedirect(redirect_url)


class UnSubscribeNewsletter(View):
    def get(self, request):
        """
        Here we want to allow user to unsubscribe to the newsletter.
        """

        SIB_NEWSLETTER_LIST_IDS = settings.SIB_NEWSLETTER_LIST_IDS.split(", ")
        SIB_NEWSLETTER_LIST_IDS = [int(i) for i in SIB_NEWSLETTER_LIST_IDS]

        user_email = self.request.user.email

        url = "https://api.sendinblue.com/v3/contacts/" + user_email

        payload = {"unlinkListIds": SIB_NEWSLETTER_LIST_IDS}

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "api-key": settings.SIB_API_KEY,
        }

        requests.request("PUT", url, json=payload, headers=headers)

        redirect_url = reverse("alert_list_view")
        return HttpResponseRedirect(redirect_url)


class InviteCollaborator(ContributorAndProfileCompleteRequiredMixin, FormView):

    form_class = InviteCollaboratorForm
    template_name = "accounts/collaborators.html"

    def form_valid(self, form):
        collaborator_email = form.cleaned_data['email']
        collaborator_last_name = form.cleaned_data['last_name']
        collaborator_first_name = form.cleaned_data['first_name']
        organization_id  = self.request.user.beneficiary_organization.id
        invitator_name = self.request.user.full_name

        users = User.objects.all()

        if users.get(email=collaborator_email):
            collaborator = users.get(email=collaborator_email)
            users.filter(pk=collaborator.pk).update(proposed_organization=organization_id)
            send_invitation_email.delay(
                collaborator.email,
                invitator_name,
                organization_id,
                collaborator_exist=True)
            track_goal(self.request.session, settings.GOAL_REGISTER_ID)
            msg = "Votre invitation a bien été envoyée ; l'utilisateur invité pourra accepter ou non votre invitation."

        else:
            collaborator = User.objects.create(
                email=collaborator_email,
                last_name=collaborator_last_name,
                first_name=collaborator_first_name,
                is_beneficiary=self.request.user.is_beneficiary,
                is_contributor=self.request.user.is_contributor,
            )
            collaborator.beneficiary_organization = self.request.user.beneficiary_organization
            collaborator_id = collaborator.pk

            # add user created to organization
            user_beneficiary_organization = self.request.user.beneficiary_organization.pk
            organizations = Organization.objects.filter(pk=user_beneficiary_organization)
            if organizations is not None:
                for organization in organizations:
                    organization.beneficiaries.add(collaborator_id)
                    organization.save()

            User.objects.filter(pk=collaborator_id).update(beneficiary_organization=organization.pk)
            send_invitation_email.delay(
                collaborator.email,
                invitator_name,
                organization_id,
                )
            track_goal(self.request.session, settings.GOAL_REGISTER_ID)

            msg = "Votre invitation a bien été envoyée."
        messages.success(self.request, msg)
        success_url = reverse("collaborators")
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        error = "erreur"
        if self.request.user.beneficiary_organization is not None:
            users = User.objects.filter(
                beneficiary_organization=self.request.user.beneficiary_organization.pk
            ).exclude(pk=self.request.user.pk)
        else:
            users = User.objects.none()
        return self.render_to_response(
            self.get_context_data(form=form, error_mail=error, users=users)
        )  # noqa


class JoinOrganization(ContributorAndProfileCompleteRequiredMixin, FormView):

    form_class = JoinOrganizationForm
    template_name = "accounts/join_organization.html"

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        user_queryset = User.objects.filter(pk=user.pk)
        proposed_organization = self.request.user.proposed_organization

        if self.request.POST.get('action') == 'no-join':
            user_queryset.update(proposed_organization = None)
            msg = "Votre refus a bien été pris en compte."
        elif self.request.POST.get('action') == 'yes-join':
            projects = form.cleaned_data['projects']
            for project in projects:
                project_queryset = Project.objects.get(pk=project.pk)
                project_queryset.organizations.remove(user.beneficiary_organization.pk)
                project_queryset.organizations.add(proposed_organization.pk)
            user_queryset.update(beneficiary_organization = user.proposed_organization.pk)
            user_queryset.update(proposed_organization = None)
            msg = f"Félicitation, vous avez rejoint l'organisation { proposed_organization }&nbsp;!"
        
        messages.success(self.request, msg)
        success_url = reverse("user_dashboard")
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.proposed_organization:
            context["organization_name"] = self.request.user.proposed_organization.name
        if self.request.user.beneficiary_organization:
            context['projects'] = Project.objects \
                .filter(organizations=self.request.user.beneficiary_organization.pk) \
                .order_by('name')
        return context


class CollaboratorsList(ContributorAndProfileCompleteRequiredMixin, ListView):
    """List of all the collaborators of an user"""

    template_name = "accounts/collaborators.html"
    context_object_name = "users"
    paginate_by = 18

    def get_queryset(self):
        if self.request.user.beneficiary_organization is not None:
            queryset = User.objects.filter(
                beneficiary_organization=self.request.user.beneficiary_organization.pk
            ).exclude(pk=self.request.user.pk)
        else:
            queryset = User.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = InviteCollaboratorForm

        return context


class CompleteProfileView(UserLoggedRequiredMixin, SuccessMessageMixin, UpdateView):
    """Complete user profile data."""

    form_class = CompleteProfileForm
    template_name = "accounts/complete_profile.html"
    success_message = "Votre profil a été mis à jour."

    def get_success_url(self):
        current_url = reverse("user_dashboard")
        next_url = self.request.GET.get("next", current_url)
        return next_url

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        """Make sure the user is not disconnected after password change."""
        res = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return res


class HistoryLoginList(ContributorAndProfileCompleteRequiredMixin, ListView):
    """List of all the connexion-logs of an user"""

    template_name = "accounts/history_login.html"
    context_object_name = "connexions"
    paginate_by = 18

    def get_queryset(self):
        if self.request.user.beneficiary_organization is not None:
            queryset = UserLastConnexion.objects.filter(
                user=self.request.user.pk
            ).order_by("-last_connexion")
        else:
            queryset = User.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DeleteHistoryLoginView(ContributorAndProfileCompleteRequiredMixin, View):
    """Allow user to delete its connexion-logs"""

    def get(self, request):

        if self.request.user:
            try:
                UserLastConnexion.objects.filter(user=self.request.user.pk).delete()
                msg = "Votre journal de connexion a bien été réinitialisé."
            except Exception:
                msg = (
                    "Une erreur s'est produite lors de la"
                    "suppression de votre journal de connexion"
                )
            messages.success(self.request, msg)
            success_url = reverse("history_login")
            return HttpResponseRedirect(success_url)
        else:
            pass
