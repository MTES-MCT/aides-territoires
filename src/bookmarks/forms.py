from django import forms
from django.utils.translation import ugettext_lazy as _

from aids.forms import AidSearchForm
from bookmarks.models import Bookmark


class UserBookmarkForm(AidSearchForm):
    """Form used to configure a new search bookmark (user connected only)."""

    title = forms.CharField(
        label=_('Give a name to your saved search'),
        required=True,
        max_length=250)
    send_email_alert = forms.BooleanField(
        label=_('Send email alert'),
        required=False)


class BookmarkAlertForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['send_email_alert']
