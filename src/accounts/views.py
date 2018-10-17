from django.views.generic import FormView
from braces.views import AnonymousRequiredMixin

from accounts.forms import LoginForm


class LoginView(AnonymousRequiredMixin, FormView):
    """Implement a simple login form."""

    template_name = 'accounts/login.html'
    form_class = LoginForm
