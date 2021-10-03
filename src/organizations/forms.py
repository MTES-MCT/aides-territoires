from django import forms

from organizations.models import Organization


class OrganizationCreateForm(forms.ModelForm):
    """allow user to create organization."""

    name = forms.CharField(
        label='Nom de votre structure',
        required=True)
    zip_code = forms.CharField(
        label='Son code postal',
        required=True)

    class Meta:
        model = Organization
        fields = ['name', 'zip_code']
