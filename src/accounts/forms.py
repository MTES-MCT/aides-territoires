from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import password_validation

from accounts.models import User


class RegisterForm(forms.ModelForm):
    """Form used to create new user accounts."""

    email = forms.EmailField(
        label=_('Your email address'),
        required=True,
        help_text=_('We will send a confirmation link to '
                    'this address before creating the account.'))
    first_name = forms.CharField(
        label=_('Your first name'),
        required=True)
    last_name = forms.CharField(
        label=_('Your last name'),
        required=True)
    ml_consent = forms.BooleanField(
        label=_('I want to receive news and communications from the service.'),
        required=False,
        help_text=_('You will be able to unsubscribe at any time.'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'ml_consent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': True})
        self.fields['email'].widget.attrs.update({
            'placeholder': _('Please double-check this value.')})

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            'Please enter a correct email address and password.'
        ),
        'inactive': _('This account is inactive.'),
    }

    username = forms.EmailField(
        label=_('Your email address'),
        required=True)
    password = forms.CharField(
        label=_('Your password'),
        required=True,
        strip=False,
        widget=forms.PasswordInput)

    def clean_username(self):
        """Don't prevent users to login when they user uppercase emails."""

        username = self.cleaned_data['username']
        return username.lower()


class PasswordResetForm(forms.Form):
    """Password reset request form."""

    username = forms.EmailField(
        label=_('Your email address'),
        required=True)


class ContributorProfileForm(forms.ModelForm):
    """Edit contributor profile related user data."""

    organization = forms.CharField(
        label=_('Your organization'),
        max_length=128,
        required=True)
    role = forms.CharField(
        label=_('Your position'),
        max_length=128,
        required=True)
    contact_phone = forms.CharField(
        label=_('Your phone number'),
        max_length=35,
        required=True)
    new_password = forms.CharField(
        label=_('Choose a new password'),
        required=False,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Leave empty to keep your existing password')
        }))

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'organization', 'role', 'contact_phone',
            'new_password',
        ]
        labels = {
            'first_name': _('Your first name'),
            'last_name': _('Your last name'),
        }

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('new_password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('new_password', error)

    def save(self, commit=True):
        user = super().save(commit=False)

        new_password = self.cleaned_data['new_password']
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()
        return user
