from django import forms

from organizations.models import Organization


class OrganizationTypeWidget(forms.SelectMultiple):
    """Custom widget for the organization_type field."""

    allow_multiple_selected = False


class OrganizationCreateForm(forms.ModelForm):
    """allow user to create organization."""

    name = forms.CharField(
        label='Nom de votre structure',
        required=True)
    zip_code = forms.CharField(
        label='Son code postal',
        required=True)
    organization_type = forms.MultipleChoiceField(
        label='Vous êtes un/une',
        required=False,
        choices=Organization.ORGANIZATION_TYPE,
        widget=OrganizationTypeWidget)

    class Meta:
        model = Organization
        fields = ['name', 'zip_code', 'organization_type']
