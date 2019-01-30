from django.views.generic import (FormView, TemplateView, RedirectView,
                                  CreateView, UpdateView)
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from braces.views import AnonymousRequiredMixin

from analytics import track_goal
from accounts.forms import (LoginForm, RegisterForm, ProfileForm,
                            ContributorProfileForm)
from accounts.tasks import send_connection_email
from accounts.models import User
from django.conf import settings


class RegisterView(AnonymousRequiredMixin, CreateView):
    """Allow users to create new messages."""

    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_success')

    def form_valid(self, form):
        """Send a connection/confirmation link to the user."""
        response = super().form_valid(form)
        user_email = form.cleaned_data['email']
        send_connection_email.delay(user_email)
        track_goal(self.request.session, settings.GOAL_REGISTER_ID)
        return response

    def form_invalid(self, form):
        """Handle invalid data provided.

        If the **only** error is that the provided email is already
        associated to an account, instead of displaying a "this user
        already exists" error, we do as if the registration proceeded
        normally and we send a connction link.
        """
        if len(form.errors) == 1 and \
           len(form['email'].errors) == 1 and \
           form['email'].errors.as_data()[0].code == 'unique':
            user_email = form.data['email']
            send_connection_email.delay(user_email)
            return HttpResponseRedirect(self.success_url)
        else:
            return super().form_invalid(form)


class RegisterSuccessView(AnonymousRequiredMixin, TemplateView):
    """Display success message after register action."""

    template_name = 'accounts/register_success.html'


class LoginRequestView(AnonymousRequiredMixin, FormView):
    """Implement a simple login form."""

    template_name = 'accounts/login_request.html'
    form_class = LoginForm
    success_url = reverse_lazy('login_sent')

    def form_valid(self, form):
        """Send a login link by email."""
        user_email = form.cleaned_data['email']
        send_connection_email.delay(user_email)
        return super().form_valid(form)


class LoginSentView(AnonymousRequiredMixin, TemplateView):
    """Simple success confirmation message."""

    template_name = 'accounts/login_sent.html'


class LoginView(AnonymousRequiredMixin, RedirectView):
    """Check token and authenticates user."""

    url = reverse_lazy('login_result')

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
                is_first_connection = user.last_login is None
                login(self.request, user)
                if is_first_connection:
                    track_goal(request.session, settings.GOAL_FIRST_LOGIN_ID)

        return super().get(request, *args, **kwargs)


class LoginResultView(TemplateView):

    def get_template_names(self):
        if self.request.user.is_authenticated:
            names = ['accounts/login_success.html']
        else:
            names = ['accounts/login_error.html']

        return names


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update profile data."""

    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_message = _('Your profile was updated successfully.')

    def get_success_url(self):
        current_url = reverse('profile')
        next_url = self.request.GET.get('next', current_url)
        return next_url

    def get_object(self):
        return self.request.user


class ContributorProfileView(LoginRequiredMixin, SuccessMessageMixin,
                             UpdateView):
    """Update contributor profile data."""

    form_class = ContributorProfileForm
    template_name = 'accounts/contributor_profile.html'
    success_message = _('Your contributor profile was updated successfully.')

    def get_success_url(self):
        current_url = reverse('contributor_profile')
        next_url = self.request.GET.get('next', current_url)
        return next_url

    def get_object(self):
        return self.request.user
