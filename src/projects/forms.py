from django import forms

from projects.models import Project
from accounts.models import User
from aids.models import Aid


class ProjectCreateForm(forms.ModelForm):
    """allow user to create project."""

    name = forms.CharField(
        label='Nom de votre projet',
        help_text='Choisissez un nom le + générique possible pour que nous puissions vous trouver des aides',
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


class ProjectMatchAidForm(forms.ModelForm):
    """allow user to associate aid to an existing project."""

    aids_associated = forms.ModelMultipleChoiceField(
        label="Aide associée au projet",
        queryset=Aid.objects.all(),
        required=False)

    class Meta:
        model = Project
        fields = ['aids_associated']
