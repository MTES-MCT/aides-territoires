from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from braces.views import AnonymousRequiredMixin

from accounts.forms import LoginForm
from accounts.tasks import send_connection_email


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
