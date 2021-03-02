from django import forms

from django.utils.translation import gettext_lazy as _

from projects.models import Project
from categories.fields import CategoryMultipleChoiceField
from categories.models import Category


class ProjectSuggestForm(forms.ModelForm):
    """form for project suggested by user."""

    CATEGORIES_QS = Category.objects \
        .select_related('theme') \
        .order_by('theme__name', 'name')

    categories = CategoryMultipleChoiceField(
        group_by_theme=True,
        label=_('Themes'),
        queryset=CATEGORIES_QS,
        to_field_name='slug',
        required=False,)

    name = forms.CharField(
        label=_('Name of your project'),
        help_text=_('Build a media library, build a bicycle road, ...'))

    description = forms.CharField(
        label=_('Describe your project in a few words'),
        widget=forms.Textarea,
        required=False,
        help_text=_('Its goal, its mobilization step or any informations'
                    ' that can identify your project'))

    class Meta:
        model = Project
        fields = ['name', 'description', 'categories']
