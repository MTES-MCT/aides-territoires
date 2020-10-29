from django.views.generic import (FormView, TemplateView, CreateView,
                                  UpdateView)
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import update_session_auth_hash
from braces.views import AnonymousRequiredMixin, MessageMixin
import requests

from analytics import track_goal
from accounts.forms import (RegisterForm, PasswordResetForm, ProfileForm,
                            ContributorProfileForm, NewsletterForm)
from accounts.tasks import send_connection_email
from accounts.models import User
from accounts.forms import NewsletterForm
from django.conf import settings


class RegisterView(AnonymousRequiredMixin, CreateView):
    """Allow users to create new accounts."""

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
                    msg = _('You are now logged in. Welcome! Please take a '
                            'few seconds to update your profile.')
                    track_goal(
                        self.request.session, settings.GOAL_FIRST_LOGIN_ID)
                else:
                    msg = _('You are now logged in. Welcome back!')

                self.messages.success(msg)
                redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
                return HttpResponseRedirect(redirect_url)

        return super().get(request, *args, **kwargs)


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

    def form_valid(self, form):
        """Make sure the user is not disconnected after password change."""

        res = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return res


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

class NewsletterView(AnonymousRequiredMixin, FormView):
    """Allow users to subscribe newsletter."""

    template_name = 'accounts/newsletter.html'
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_success')

    def get_Newsletter_user(self):
        if self.request.method == 'POST':
            form = NewsletterForm(self.request.POST)
            if form.is_valid():
                self.export_account(form.cleaned_data['email'])
                return HttpResponseRedirect('/newsletter_success/')
        else:
            form = NewsletterForm()

    def export_account(self, user):
        '''Export newsletterUser to the newsletter provider'''

        API_HEADERS = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'api-key': settings.SIB_API_KEY,
        }
        
        endpoint = 'https://api.sendinblue.com/v3/contacts/'
        data = {
            'email': user,
            'attributes': {
                'DOUBLE_OPT-IN': 1,
            },
            'listIds': [settings.SIB_LIST_ID],
            'updateEnabled': True,
        }
        requests.post(endpoint, headers=API_HEADERS, data=data)
        self.stdout.write('Exporting {}'.format(user))


class NewsletterSuccessView(AnonymousRequiredMixin, TemplateView):
    """Display success message after register action."""

    template_name = 'accounts/newsletter_success.html'
