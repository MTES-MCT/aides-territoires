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
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import resolve_url, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.db.models.query import QuerySet


from braces.views import AnonymousRequiredMixin, MessageMixin

from accounts.mixins import (
    ContributorAndProfileCompleteRequiredMixin,
    UserLoggedRequiredMixin,
)
from accounts.forms import (
    RegisterForm,
    RegisterCommuneForm,
    PasswordResetForm,
    PasswordResetConfirmForm,
    ContributorProfileForm,
    InviteCollaboratorForm,
    CompleteProfileForm,
    JoinOrganizationForm,
)
from accounts.tasks import (
    send_connection_email,
    send_invitation_email,
    send_reject_invitation_email,
    send_accept_invitation_email,
    send_welcome_email,
    send_leave_organization_email,
)
from accounts.models import User, UserLastConnexion
from aids.resources import ADMIN_EMAIL
from projects.models import Project
from aids.models import Aid, AidProject
from organizations.models import Organization
from geofr.models import Perimeter

from analytics.utils import track_goal
from alerts.models import Alert


class RegisterView(AnonymousRequiredMixin, CreateView):
    """Allow users to create new accounts."""

    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("register_success")

    def form_valid(self, form):
        organization_name = self.request.POST.get("organization_name", None)
        organization_perimeter_id = int(
            self.request.POST.get("perimeter", None).partition("-")[0]
        )
        organization_perimeter = Perimeter.objects.get(id=organization_perimeter_id)
        organization_type = self.request.POST.get("organization_type", None)

        user = form.save(commit=False)
        organization = Organization.objects.create(
            name=organization_name,
            organization_type=[organization_type],
            perimeter=organization_perimeter,
        )
        user.beneficiary_organization = organization
        user.save()
        organization.beneficiaries.add(user.pk)

        user.send_notification(
            title="Bienvenue sur Aides-territoires !",
            message=f"""
            <p>Bienvenue sur Aides-territoires !</p>
            <p>
                Vous venez de créer votre compte et devriez avoir reçu un courrier
                électronique présentant notre site.
            </p>
            <p>
                Si ce n’est pas le cas, n’hésitez pas à
                <a href="{reverse('contact')}">nous contacter</a>.
            </p>
            <p>
                Vous pouvez paramétrer les notifications que vous souhaitez recevoir
                via <a href="{reverse('notification_settings_view')}">
                vos préférences
                </a>.
            </p>
            """,
        )

        response = super().form_valid(form)
        send_connection_email.delay(user.email)
        track_goal(self.request.session, settings.GOAL_REGISTER_ID)
        msg = "Vous êtes bien enregistré !"
        messages.success(self.request, msg)

        return response

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        return context


class RegisterCommuneView(AnonymousRequiredMixin, CreateView):
    """Allow mayors and staff of communes to quickly create an account and organization."""

    template_name = "accounts/register_commune.html"
    form_class = RegisterCommuneForm
    success_url = reverse_lazy("register_success")

    def form_valid(self, form):

        organization_name = self.request.POST.get("organization_name", None)
        organization_perimeter_id = int(
            self.request.POST.get("perimeter", None).partition("-")[0]
        )
        organization_perimeter = Perimeter.objects.get(id=organization_perimeter_id)

        user = form.save(commit=False)
        organization = Organization.objects.create(
            name=organization_name,
            organization_type=["commune"],
            perimeter=organization_perimeter,
        )
        user.beneficiary_organization = organization

        user.save()
        organization.beneficiaries.add(user.pk)

        response = super().form_valid(form)
        send_connection_email.delay(user.email)
        track_goal(self.request.session, settings.GOAL_REGISTER_ID)
        msg = "Vous êtes bien enregistré !"
        messages.success(self.request, msg)

        return response


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
    UserLoggedRequiredMixin, SuccessMessageMixin, UpdateView
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

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()

        if user.notification_counter == 0:
            user.send_notification(
                title="Mise en place du système de notifications",
                message=f"""
                <p>
                    Bienvenue dans le nouveau système de notifications
                    d’Aides-territoires !
                </p>
                <p>
                    Vous recevrez bientôt des notifications liées à vos aides,
                    mais aussi à votre structure ou à vos projets.
                </p>

                <p>
                    Vous pouvez paramétrer la fréquence des notifications via
                    <a href="{reverse('notification_settings_view')}">vos préférences</a>.
                </p>
                """,
            )

        return super().form_valid(form)


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
        Here we want to allow user to subscribe to the newsletter.
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
            msg = """
                Votre demande d’inscription à la newsletter a bien été prise en compte.<br />
                <strong>Afin de finaliser votre inscription il vous reste à cliquer sur le lien
                de confirmation présent dans l’e-mail que vous allez recevoir.</strong>
                """
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

    # We add request as kwargs to access self.request.user in the form's clean_email def
    def get_form_kwargs(self):
        kwargs_form = super(InviteCollaborator, self).get_form_kwargs()
        kwargs_form["request"] = self.request
        return kwargs_form

    def form_valid(self, form):
        collaborator_email = form.cleaned_data["email"]
        collaborator_last_name = form.cleaned_data["last_name"]
        collaborator_first_name = form.cleaned_data["first_name"]
        organization_id = self.request.user.beneficiary_organization.id
        invitation_author = self.request.user.full_name

        users = User.objects.all()

        if users.filter(email=collaborator_email).exists():
            collaborator = users.get(email=collaborator_email)
            users.filter(pk=collaborator.pk).update(
                proposed_organization=organization_id
            )
            users.filter(pk=collaborator.pk).update(
                invitation_author=self.request.user.pk, invitation_date=timezone.now()
            )
            send_invitation_email.delay(
                collaborator.email,
                invitation_author,
                organization_id,
                collaborator_exist=True,
            )
            track_goal(self.request.session, settings.GOAL_REGISTER_ID)
            msg = "Votre invitation a bien été envoyée ; l’utilisateur invité pourra accepter ou non votre invitation."  # noqa

        else:
            collaborator = User.objects.create(
                email=collaborator_email,
                last_name=collaborator_last_name,
                first_name=collaborator_first_name,
                is_beneficiary=self.request.user.is_beneficiary,
                is_contributor=self.request.user.is_contributor,
                acquisition_channel=User.ACQUISITION_CHANNEL_CHOICES.invited,
            )
            collaborator.beneficiary_organization = (
                self.request.user.beneficiary_organization
            )
            collaborator_id = collaborator.pk

            # add user created to organization
            user_beneficiary_organization = (
                self.request.user.beneficiary_organization.pk
            )
            organizations = Organization.objects.filter(
                pk=user_beneficiary_organization
            )
            if organizations is not None:
                for organization in organizations:
                    organization.beneficiaries.add(collaborator_id)
                    organization.save()

            User.objects.filter(pk=collaborator_id).update(
                beneficiary_organization=organization.pk
            )
            send_invitation_email.delay(
                collaborator.email,
                invitation_author,
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
        )


class JoinOrganization(ContributorAndProfileCompleteRequiredMixin, FormView):

    form_class = JoinOrganizationForm
    template_name = "accounts/join_organization.html"

    @transaction.atomic
    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        user_queryset = User.objects.filter(pk=user.pk)
        proposed_organization = self.request.user.proposed_organization
        invitation_author = self.request.user.invitation_author

        if "no-join" in self.request.POST:
            send_reject_invitation_email.delay(
                invitation_author.email, user.full_name, proposed_organization.pk
            )
            track_goal(self.request.session, settings.GOAL_REGISTER_ID)
            user_queryset.update(proposed_organization=None)

            invitation_author.send_notification(
                title="Votre invitation a été refusée",
                message=f"""
                <p>
                    {user.full_name} a refusé votre invitation.
                </p>
                """,
            )
            msg = "Votre refus a bien été pris en compte. Un email indiquant votre refus a été envoyé."  # noqa
        elif "yes-join" in self.request.POST:
            projects = form.cleaned_data["projects"]
            collaborators = form.cleaned_data["collaborators"]

            # Duplicate selected projects & Transfer them to the proposed_organization
            for project in projects:
                project_queryset = Project.objects.get(pk=project.pk)
                project_description = project_queryset.description
                project_name = project_queryset.name

                duplicate_project = Project.objects.create(
                    name=project_name,
                    description=project_description,
                )
                duplicate_project.author.add(self.request.user.pk)
                duplicate_project.organizations.add(proposed_organization)
                aidproject_list = AidProject.objects.filter(project=project_queryset.pk)
                for aidproject in aidproject_list:
                    AidProject.objects.create(
                        aid=aidproject.aid,
                        project=duplicate_project,
                        creator=self.request.user,
                    )

            # if the author of the project is the user,
            # and if the current organization has more than one beneficiary
            # we reattribute the project to an other user of the current organization
            organization_projects = Project.objects.filter(
                organizations=user.beneficiary_organization.pk
            )
            for project in organization_projects:
                if project.author.first() == user:
                    if (
                        Organization.objects.get(
                            pk=user.beneficiary_organization.pk
                        ).beneficiaries.count()
                        > 1
                    ):
                        new_author = (
                            User.objects.filter(
                                beneficiary_organization=user.beneficiary_organization.pk
                            )
                            .exclude(pk=user.pk)
                            .first()
                        )
                        project.author.add(new_author.pk)
                        project.author.remove(user.pk)

            # Send an invitation to selected collaborators
            # and populate proposed_organization field for each selected collaborators
            for collaborator in collaborators:
                collaborator = User.objects.get(pk=collaborator.pk)
                User.objects.filter(pk=collaborator.pk).update(
                    proposed_organization=proposed_organization,
                    invitation_author=self.request.user.pk,
                    invitation_date=timezone.now(),
                )
                send_invitation_email.delay(
                    collaborator.email,
                    user.full_name,
                    proposed_organization.pk,
                    collaborator_exist=True,
                )
                track_goal(self.request.session, settings.GOAL_REGISTER_ID)

            # Remove user from his current organization
            # if current organization has no user :
            # delete the organization, AidProject & Projects objects associated
            user_current_org = Organization.objects.get(
                pk=user.beneficiary_organization.pk
            )
            if user_current_org.beneficiaries.count() == 1:
                projects = Project.objects.filter(
                    organizations=user.beneficiary_organization.pk
                )
                for project in projects:
                    AidProject.objects.filter(project=project).delete()
                projects.delete()
                user_queryset.update(
                    beneficiary_organization=user.proposed_organization.pk
                )
                user_current_org.beneficiaries.remove(user.pk)
                user_current_org.delete()
            else:
                # send an email to all the former collaborators to inform them
                # that user leave the organization
                former_collaborators = User.objects.filter(
                    beneficiary_organization=user.beneficiary_organization.pk
                ).exclude(pk=user.pk)
                for former_collaborator in former_collaborators:
                    former_collaborator.send_notification(
                        title="Un collaborateur quitte votre structure",
                        message=f"""
                        <p>
                            {user.full_name} a quitté votre structure {user_current_org.name}.
                        </p>
                        """,
                    )

                    send_leave_organization_email.delay(
                        former_collaborator.email,
                        user.full_name,
                        former_collaborator.beneficiary_organization.pk,
                    )
                    track_goal(self.request.session, settings.GOAL_REGISTER_ID)
                # change user organization
                user_queryset.update(
                    beneficiary_organization=user.proposed_organization.pk
                )
                # remove user from organization object
                Organization.objects.get(
                    pk=user.beneficiary_organization.pk
                ).beneficiaries.remove(user.pk)

            # Add user to the proposed_organization
            Organization.objects.get(
                pk=user.proposed_organization.pk
            ).beneficiaries.add(user.pk)
            user_queryset.update(proposed_organization=None)

            # Add join_organization_date
            User.objects.filter(pk=user.pk).update(
                join_organization_date=timezone.now(),
            )

            # Send an email to the invitation_author to notice user joined the organization
            send_accept_invitation_email.delay(
                invitation_author.email, user.full_name, proposed_organization.pk
            )
            track_goal(self.request.session, settings.GOAL_REGISTER_ID)

            # Send a notification to the invitation_author and other members
            invitation_author.send_notification(
                title="Votre invitation a été acceptée",
                message=f"""
                <p>
                    {user.full_name} a accepté votre invitation et vient de
                    rejoindre votre structure {proposed_organization.name}.
                </p>
                """,
            )
            other_members = proposed_organization.beneficiaries.exclude(
                id__in=[user.id, invitation_author.id]
            )
            for member in other_members:
                member.send_notification(
                    title="Une invitation a été acceptée",
                    message=f"""
                    <p>
                        {user.full_name} a accepté l’invitation de {invitation_author.full_name}
                        et vient de rejoindre votre structure {proposed_organization.name}.
                    </p>
                    """,
                )

            msg = f"Félicitations, vous avez rejoint la structure { proposed_organization } !"

        messages.success(self.request, msg)
        success_url = reverse("user_dashboard")
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.proposed_organization:
            context["organization_name"] = self.request.user.proposed_organization.name
            context["invitation_author"] = self.request.user.invitation_author.full_name
        if self.request.user.beneficiary_organization:
            context["projects"] = Project.objects.filter(
                organizations=self.request.user.beneficiary_organization.pk
            ).order_by("name")
            context["collaborators"] = (
                User.objects.filter(
                    beneficiary_organization=self.request.user.beneficiary_organization.pk
                )
                .exclude(pk=self.request.user.pk)
                .order_by("last_name")
            )
        return context


class CollaboratorsList(ContributorAndProfileCompleteRequiredMixin, ListView):
    """List of all the collaborators of an user"""

    template_name = "accounts/collaborators.html"
    context_object_name = "users"
    paginate_by = 18

    def get_queryset(self):
        beneficiary_organization_pk = self.request.user.beneficiary_organization.pk
        if self.request.user.beneficiary_organization is not None:
            queryset = User.objects.filter(
                Q(beneficiary_organization=beneficiary_organization_pk)
                | Q(proposed_organization=beneficiary_organization_pk)
            ).exclude(pk=self.request.user.pk)
        else:
            queryset = User.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = InviteCollaboratorForm
        context["beneficiary_organization"] = self.request.user.beneficiary_organization

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


class DeleteUserView(UserLoggedRequiredMixin, TemplateView):
    """
    Asks the user what to do with their user-generated content
    before deleting their profile.
    """

    template_name = "accounts/user_delete_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        user_org = self.request.user.organization_set.first()

        context["organization"] = user_org
        context["organization_members"] = user_org.beneficiaries.exclude(id=user.id)
        context["projects"] = user_org.project_set.filter(author=user)

        context["alerts"] = Alert.objects.filter(email=user.email)
        context["aids"] = Aid.objects.filter(author=user)
        context["invitations"] = User.objects.filter(invitation_author_id=user)

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        See the function manage_user_content_before_deletion in accounts/models.py
        for a detailed explanation the logic
        """

        post_data = request.POST
        user = request.user
        user_org = user.beneficiary_organization
        user_org_members = user_org.beneficiaries.exclude(id=user.id)

        alerts = Alert.objects.filter(email=user.email)
        for alert in alerts:
            if f"alert-{alert.pk}" in post_data:
                alert.delete()

        at_admin, _created = User.objects.get_or_create(email=ADMIN_EMAIL)

        if "invitations-transfer" in post_data:
            new_inviter_id = post_data["invitations-transfer"]
            new_inviter = get_object_or_404(user_org_members, pk=new_inviter_id)
            self.transfer_invitations(user, new_inviter)

        if "projects-transfer" in post_data:
            # At this step, we check if the user explicitely set a new author
            # If they didn't and there are other users in the org, authorship
            # will be transferred to the first available user
            new_author_id = post_data["projects-transfer"]
            new_author = get_object_or_404(user_org_members, pk=new_author_id)

            self.transfer_projects(user, new_author)

        # If the user is alone or has not chosen a new author,
        # aids are reattributed to the AT admin account.
        # aids are protected and so must be processed before the delete() is called.
        aids = Aid.objects.filter(author=user)
        if "aids-transfer" in post_data:
            new_author_id = post_data["aids-transfer"]
            new_author = get_object_or_404(user_org_members, pk=new_author_id)

            self.transfer_aids(aids, new_author)
        else:
            self.transfer_aids(aids, at_admin)

        user.delete()

        messages.success(request, "Votre compte utilisateur a été supprimé.")
        return redirect("/")

    def transfer_invitations(self, user: User, new_inviter: User) -> None:
        """Helper method to transfer the invitations"""
        invited_users = User.objects.filter(invitation_author_id=user)

        for invited_user in invited_users:
            invited_user.invitation_author_id = new_inviter
            invited_user.save()

    def transfer_projects(self, user: User, new_author: User) -> None:
        """Helper method to transfer the projects"""
        user_org = user.beneficiary_organization
        projects = user_org.project_set.filter(author=user)

        if new_author:
            for project in projects:
                project.author.add(new_author)
                project.save()

    def transfer_aids(self, aids: QuerySet, new_author: User) -> None:
        """Helper method to transfer the projects"""
        for aid in aids:
            aid.author = new_author
            aid.save()


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
                    "Une erreur s’est produite lors de la"
                    "suppression de votre journal de connexion"
                )
            messages.success(self.request, msg)
            success_url = reverse("history_login")
            return HttpResponseRedirect(success_url)
        else:
            pass
