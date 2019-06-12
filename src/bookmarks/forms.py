from django import forms

from bookmarks.models import Bookmark


class BookmarkAlertForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['send_email_alert']
