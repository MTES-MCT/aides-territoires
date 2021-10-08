from django.conf import settings
from django.views.generic import FormView, TemplateView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.http import urlsafe_base64_decode

from braces.views import AnonymousRequiredMixin, MessageMixin

from accounts.mixins import ContributorAndProfileCompleteRequiredMixin
from accounts.forms import RegisterForm, PasswordResetForm, ContributorProfileForm
from accounts.tasks import send_connection_email, send_welcome_email
from accounts.models import User
from analytics.utils import track_goal


class RegisterView(AnonymousRequiredMixin, CreateView):
    """Allow users to create new accounts."""

    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('organization_create_view')

    def form_valid(self, form):
        """Send a connection/confirmation link to the user."""
        user_email = form.cleaned_data['email']
        user_first_name = form.cleaned_data['first_name']
        user_last_name = form.cleaned_data['last_name']
        self.request.session['USER_EMAIL'] = user_email
        self.request.session['USER_NAME'] = user_first_name + ' ' + user_last_name
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle invalid data provided.

        If the **only** error is that the provided email is already
        associated to an account, instead of displaying a "this user
        already exists" error, we do as if the registration proceeded
        normally and we send a connection link.
        """
        if len(form.errors) == 1 and \
           len(form['email'].errors) == 1 and \
           form['email'].errors.as_data()[0].code == 'unique':
            redirect_url = reverse('register_success')
            return HttpResponseRedirect(redirect_url)
        else:
            return super().form_invalid(form)


class RegisterSuccessView(AnonymousRequiredMixin, TemplateView):
    """Display success message after register action."""

    template_name = 'accounts/register_success.html'


class PasswordResetView(AnonymousRequiredMixin, FormView):
    """Implement a simple login form using email only."""

    template_name = 'accounts/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_sent')

    def form_valid(self, form):
        """Send a login link by email."""
        user_email = form.cleaned_data['username']
        send_connection_email.delay(user_email)
        return super().form_valid(form)


class PasswordResetSentView(AnonymousRequiredMixin, TemplateView):
    """Simple success confirmation message."""

    template_name = 'accounts/password_reset_sent.html'


class TokenLoginView(AnonymousRequiredMixin, MessageMixin, TemplateView):
    """Check token and authenticates user."""

    template_name = 'accounts/login_error.html'

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (ValueError, User.DoesNotExist):
            user = None

        if user:
            token = kwargs['token']
            if default_token_generator.check_token(user, token):
                is_first_login = user.last_login is None
                login(self.request, user)

                if is_first_login:
                    msg = 'Vous êtes maintenant connecté. Bienvenue ! Pourriez-vous prendre quelques secondes pour mettre à jour votre profil ?'  # noqa
                    track_goal(self.request.session, settings.GOAL_FIRST_LOGIN_ID)
                    send_welcome_email.delay(user.email)
                else:
                    msg = 'Vous êtes maintenant connecté. Bienvenue !'

                self.messages.success(msg)
                redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
                return HttpResponseRedirect(redirect_url)

        return super().get(request, *args, **kwargs)


class ContributorProfileView(ContributorAndProfileCompleteRequiredMixin,
                             SuccessMessageMixin, UpdateView):
    """Update contributor profile data."""

    form_class = ContributorProfileForm
    template_name = 'accounts/contributor_profile.html'
    success_message = 'Votre profil a été mis à jour.'

    def get_success_url(self):
        current_url = reverse('user_dashboard')
        next_url = self.request.GET.get('next', current_url)
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

    template_name = 'accounts/user_dashboard.html'


class UserApiTokenView(ContributorAndProfileCompleteRequiredMixin, TemplateView):
    """User can access to his API Token"""

    template_name = 'accounts/user_api_token.html'
