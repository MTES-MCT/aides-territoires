from django import forms

from dsfr.forms import DsfrBaseForm
from core.forms import RichTextField

from projects.models import Project
from organizations.models import Organization


class ProjectCreateForm(forms.ModelForm, DsfrBaseForm):
    """allow user to create project."""

    name = forms.CharField(label="Nom de votre projet", required=True)
    description = RichTextField(
        label="Description du projet",
        required=False,
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

    class Meta:
        model = Project
        fields = ["name", "description", "organizations", "due_date"]


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

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "due_date",
        ]
        widgets = {
            "due_date": forms.TextInput(
                attrs={"type": "date", "placeholder": "jj/mm/aaaa"}
            ),
        }


class ProjectExportForm(forms.ModelForm):
    """Form used to export a project."""

    CHOICES = [
        ("csv", "Fichier CSV"),
        ("xlsx", "Tableur Excel"),
    ]
    # ("pdf", "Document PDF"),

    format = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="Veuillez sélectionner le format d’export :",
    )

    class Meta:
        model = Project
        fields = ["format"]
