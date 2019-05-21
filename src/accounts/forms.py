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
        self.fields['email'].widget.attrs.update({
            'placeholder': _('Please double-check this value.')})


class LoginForm(AuthenticationForm):

    """Simple login form with no password."""

    username = forms.EmailField(
        label=_('Your email address'),
        required=True)
    password = forms.CharField(
        label=_('Your password'),
        required=True,
        strip=False,
        widget=forms.PasswordInput)


class PasswordResetForm(forms.Form):
    """Password reset request form."""

    username = forms.EmailField(
        label=_('Your email address'),
        required=True)


class ProfileForm(forms.ModelForm):
    """Edit profile related user data."""

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
        fields = ['full_name', 'new_password', 'ml_consent']
        labels = {
            'full_name': _('Your full name'),
            'ml_consent':
                _('Yes, I want to receive news about the service.'),
        }
        help_texts = {
            'full_name':
                _('This is how we will address you in our ' 'communications.'),
            'ml_consent':
                _('We will send regular updates (no more than once a month) '
                  'about the new features and updates about our service.'),
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


class ContributorProfileForm(forms.ModelForm):
    """Edit contributor profile related user data."""

    class Meta:
        model = User
        fields = ['organization', 'role', 'contact_phone']
        labels = {
            'organization': _('Your organization'),
            'role': _('Your position'),
        }
