from django import forms

from projects.models import Project
from accounts.models import User


class ProjectCreateForm(forms.ModelForm):
    """allow user to create project."""

    name = forms.CharField(
        label='Nom de votre projet',
        help_text="Choisissez un nom le + générique possible \
            pour que nous puissions vous trouver des aides",
        required=True)

    beneficiary = forms.ModelMultipleChoiceField(
        label="Créateur du projet",
        queryset=User.objects.all(),
        required=False)

    due_date = forms.DateTimeField(
        label="Date d'échéance",
        help_text='Si votre projet doit sortir avant une certaine date, indiquez-la ici',
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date', 'placeholder': 'jj/mm/aaaa'}))

    class Meta:
        model = Project
        fields = ['name', 'beneficiary', 'due_date']
