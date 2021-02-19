from django import forms

from projects.models import Project


class ProjectSuggestForm(forms.ModelForm):
    """form for project suggested by user."""

    class Meta:
        model = Project
        fields = ['name', 'description']

    def clean_name(self):
        data = self.cleaned_data['name']

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        return data
