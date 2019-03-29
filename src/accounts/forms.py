from django import forms
from django.utils.translation import ugettext_lazy as _

from tags.fields import TagChoiceField
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

    watched_tags = TagChoiceField(
        label=_('Your watched tags'),
        help_text=_('This is the list of topics you are interested in.')
    )

    class Meta:
        model = User
        fields = ['ml_consent', 'similar_aids_alert', 'watched_tags']
        labels = {
            'ml_consent':
                _('Yes, I want to receive news about the service.'),
            'similar_aids_alert':
                _('Yes, I want to receive alerts when similar new aids '
                  'are published.'),
        }
        help_texts = {
            'ml_consent':
                _('We will send regular updates (no more than once a month) '
                  'about the new features and updates about our service.'),
            'similar_aids_alert':
                _('We will detect when newly published aids are similar '
                  'to the ones you saved into one of your lists, and send '
                  'you an e-mail alert when it happens.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # We set the existing tags as the `choices` value so the existing
        # tags will be displayed in the widget
        all_tags = self.instance.watched_tags
        if self.is_bound:
            if hasattr(self.data, 'getlist'):
                all_tags += self.data.getlist('watched_tags')
            else:
                all_tags += self.data.get('watched_tags', [])
        self.fields['watched_tags'].choices = zip(all_tags, all_tags)


class ContributorProfileForm(forms.ModelForm):
    """Edit contributor profile related user data."""

    class Meta:
        model = User
        fields = ['organization', 'role', 'contact_phone']
        labels = {
            'organization': _('Your organization'),
            'role': _('Your position'),
        }
