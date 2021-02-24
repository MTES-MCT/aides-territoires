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

    class Meta:
        model = Project
        fields = ['name', 'description', 'categories']

    def clean_name(self):
        data = self.cleaned_data['name']

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        return data
