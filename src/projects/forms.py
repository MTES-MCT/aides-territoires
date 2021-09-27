from django import forms

from core.forms import (RichTextField)

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


class ProjectUpdateForm(forms.ModelForm):

    name = forms.CharField(
        label='Nom du projet',
        max_length=256,
        required=True)
    description = RichTextField(
        label="Description du projet",
        widget=forms.Textarea(
            attrs={'placeholder': "Entrez ici la description de votre projet"}
        ))
    due_date = forms.DateField(
        label="Date d'échéance du projet",
        ),

    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'due_date',
        ]
        widgets = {
            'due_date': forms.TextInput(
                attrs={'type': 'date', 'placeholder': 'jj/mm/aaaa'}),
        }
