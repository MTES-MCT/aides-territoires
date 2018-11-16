from django import forms
from django.utils.translation import ugettext_lazy as _

from core.forms.widgets import MultipleChoiceFilterWidget


class BookmarkForm(forms.Form):
    bundles = forms.ModelMultipleChoiceField(
        label=_('Add this aid to the following bundles:'),
        queryset=None,
        required=False,
        widget=MultipleChoiceFilterWidget)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['bundles'].queryset = self.user.bundles.all()