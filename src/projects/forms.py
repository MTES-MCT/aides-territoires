from django import forms

from dsfr.forms import DsfrBaseForm

from projects.constants import EXPORT_FORMAT_CHOICES
from core.forms import (
    AutocompleteModelChoiceField,
    RichTextField,
)

from projects.models import Project
from organizations.models import Organization
from keywords.models import SynonymList


class ProjectCreateForm(forms.ModelForm, DsfrBaseForm):
    """allow user to create project."""

    name = forms.CharField(label="Nom de votre projet", required=True)
    description = RichTextField(
        label="Description du projet",
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Entrez ici la description de votre projet"}
        ),
    )
    organizations = forms.ModelMultipleChoiceField(
        label="Créateur du projet", queryset=Organization.objects.all(), required=False
    )
    due_date = forms.DateTimeField(
        label="Date d’échéance",
        help_text="Si votre projet doit sortir avant une certaine date, indiquez-la ici",
        required=False,
        widget=forms.TextInput(attrs={"type": "date", "placeholder": "jj/mm/aaaa"}),
    )
    project_types = AutocompleteModelChoiceField(
        label="Types de projet", queryset=SynonymList.objects.all(), required=False
    )
    project_types_suggestion = forms.CharField(
        label="Type de projet suggéré",
        help_text="Suggérez-nous un type de projet qui ne semble pas être présent dans la liste des types de projets.",
        required=False,
    )
    is_public = forms.BooleanField(
        label="Souhaitez-vous rendre ce projet public sur Aides-territoires?",
        help_text="Les informations de votre structure doivent avoir été complétées afin que ce choix soit possible.",
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "organizations",
            "due_date",
            "project_types",
            "project_types_suggestion",
            "is_public",
        ]


class ProjectUpdateForm(forms.ModelForm, DsfrBaseForm):

    name = forms.CharField(label="Nom du projet", max_length=256, required=True)
    description = RichTextField(
        label="Description du projet",
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Entrez ici la description de votre projet"}
        ),
    )
    due_date = (
        forms.DateField(
            label="Date d’échéance du projet",
        ),
    )
    project_types = AutocompleteModelChoiceField(
        label="Types de projet", queryset=SynonymList.objects.all(), required=False
    )
    project_types_suggestion = forms.CharField(
        label="Type de projet suggéré",
        help_text="Suggérez-nous un type de projet qui ne semble pas être présent dans la liste des types de projets.",
        required=False,
    )
    is_public = forms.BooleanField(
        label="Souhaitez-vous rendre ce projet public sur Aides-territoires?",
        help_text="Les informations de votre structure doivent avoir été complétées afin que ce choix soit possible.",
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "due_date",
            "project_types",
            "project_types_suggestion",
            "is_public",
        ]
        widgets = {
            "due_date": forms.TextInput(
                attrs={"type": "date", "placeholder": "jj/mm/aaaa"}
            ),
        }


class ProjectExportForm(forms.ModelForm):
    """Form used to export a project."""

    CHOICES = EXPORT_FORMAT_CHOICES

    format = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="Veuillez sélectionner le format d’export :",
    )

    class Meta:
        model = Project
        fields = ["format"]
