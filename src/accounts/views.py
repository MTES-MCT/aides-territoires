from django.views.generic import FormView, TemplateView, RedirectView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from braces.views import AnonymousRequiredMixin


from accounts.forms import LoginForm
from accounts.tasks import send_connection_email
from accounts.models import User


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
                login(self.request, user)

        return super().get(request, *args, **kwargs)


class LoginResultView(TemplateView):

    def get_template_names(self):
        if self.request.user.is_authenticated:
            names = ['accounts/login_success.html']
        else:
            names = ['accounts/login_error.html']

        return names
