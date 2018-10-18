from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    """Simple login form with no password."""

    email = forms.EmailField(
        label=_('Your email address'),
        required=True)
