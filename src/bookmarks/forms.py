from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from aids.forms import AidSearchForm
from bookmarks.models import Bookmark


class UserBookmarkForm(AidSearchForm):
    """Form used to configure a new search bookmark (user connected only)."""

    title = forms.CharField(
        label=_('Give a name to your bookmarked search'),
        required=True,
        max_length=250)
    send_email_alert = forms.BooleanField(
        label=_('Receive new results by email'),
        required=False)


class AnonymousBookmarkForm(AidSearchForm):
    """Configure new search bookmarks (anonymous users only)."""

    title = forms.CharField(
        label=_('Give a name to your bookmarked search'),
        required=True,
        max_length=250)
    email = forms.EmailField(
        label=_('Your email address'),
        help_text=_('We will send an email to confirm your address'),
        required=True)

    def clean_email(self):
        """Make sure the email is not linked to an existing account."""

        email = self.cleaned_data['email']
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            msg = _('An account with this address already exists. If this is '
                    'your account, you might want to login first.')
            raise forms.ValidationError(msg, code='unique')
        return email


class BookmarkAlertForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['send_email_alert']
