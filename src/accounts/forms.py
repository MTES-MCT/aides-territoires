from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class LoginForm(forms.Form):
    """Simple login form with no password."""

    email = forms.EmailField(
        label=_('Your email address'),
        required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': True})


class RegisterForm(forms.ModelForm):
    """Form used to create new user accounts."""

    email = forms.EmailField(
        label=_('Your email address'),
        required=True,
        help_text=_('We will send a confirmation link to '
                    'this address before creating the account.'))
    full_name = forms.CharField(
        label=_('Your full name'),
        required=True,
        help_text=_('This is how we will address you in our communications.'))
    ml_consent = forms.BooleanField(
        label=_('I want to receive news and communications from the service.'),
        required=False,
        help_text=_('You will be able to unsubscribe at any time.'))

    class Meta:
        model = User
        fields = ['full_name', 'email', 'ml_consent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'autofocus': True})


class ProfileForm(forms.ModelForm):
    """Edit profile related user data."""

    ml_consent = forms.BooleanField(
        required=False,
        label=_('Yes, I want to receive news about the service.'),
        help_text=_('We will send regular updates (no more than once a month) '
                    'about the new features and updates about our service.'))
    similar_aids_alert = forms.BooleanField(
        required=False,
        label=_('Yes, I want to receive alerts when similar new aids '
                'are published.'),
        help_text=_('We will detect when newly published aids are similar to '
                    'the ones you saved into one of your lists, and send you '
                    'an e-mail alert when it happens.'))

    class Meta:
        model = User
        fields = ['organization', 'role', 'contact_phone', 'ml_consent',
                  'similar_aids_alert']
