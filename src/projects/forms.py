from django import forms

from core.forms import (
    AutocompleteModelChoiceField, AutocompleteModelMultipleChoiceField,
    MultipleChoiceFilterWidget, RichTextField)
from projects.models import Project
from categories.fields import CategoryMultipleChoiceField
from categories.models import Category, Theme

class SuggestedProjectForm(forms.ModelForm):
    """form for project suggested by user."""

    CATEGORIES_QS = Category.objects \
        .select_related('theme') \
        .order_by('theme__name', 'name')

    name = forms.CharField(
        label=_('Project title'),
        required=False,
        max_length=64,
        widget=forms.TextInput(
            attrs={'placeholder': _('Build a library')}
        ))
    description = RichTextField(
        label=_('Full description of the project'),
        widget=forms.Textarea(attrs={'placeholder': _(
            'If you have a description, do not hesitate to copy it here.\n'
            'Try to complete the description with the maximum of'
            ' information.\n')}))
    categories = CategoryMultipleChoiceField(
        label=_('Aid categories'),
        help_text=_('Choose one or several categories that match your aid.'),
        required=False)
