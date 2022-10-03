from django import forms

from dsfr.forms import DsfrBaseForm

from projects.constants import EXPORT_FORMAT_CHOICES
from core.forms import (
    AutocompleteModelMultipleChoiceField,
    RichTextField,
)

from projects.models import Project
from organizations.models import Organization
from keywords.models import SynonymList


class ProjectCreateForm(forms.ModelForm, DsfrBaseForm):
    """allow user to create project."""

    name = forms.CharField(
        label="Nom de votre projet",
        required=True,
        help_text=(
            "Donnez un nom explicite : préférez 'végétalisation du quartier des coteaux' \
             à 'quartier des coteaux'"
        ),
    )
    description = RichTextField(
        label="Description de votre projet",
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Entrez ici une description plus précise de votre projet"
            }
        ),
    )
    private_description = RichTextField(
        label="Notes internes de votre projet",
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Informations réservées à vos collaborateurs."}
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
    project_types = AutocompleteModelMultipleChoiceField(
        label="Types de projet",
        queryset=SynonymList.objects.all(),
        required=False,
        help_text=(
            "Cette information nous aide à identifier les meilleures aides pour votre projet, \
             et à le retrouver plus facilement. Si vous ne trouvez pas le type de projet qui vous \
              correspond, vous pouvez en proposer un nouveau dans le champ 'Autre type de projet'."
        ),
    )
    project_types_suggestion = forms.CharField(
        label="Autre type de projet",
        help_text="Suggérez-nous un autre type de projet",
        required=False,
    )
    contract_link = forms.ChoiceField(
        label="Appartenance à un plan/programme/contrat",
        required=False,
    )
    is_public = forms.BooleanField(
        label="Souhaitez-vous rendre ce projet public sur Aides-territoires?",
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "private_description",
            "organizations",
            "due_date",
            "project_types",
            "project_types_suggestion",
            "contract_link",
            "is_public",
        ]

    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.fields["contract_link"].choices = [
            ("", "Ce projet appartient-il à un programme?")
        ] + Project.CONTRACT_LINK

    def clean(self):
        data = super().clean()
        if not any((data.get("project_types"), data.get("project_types_suggestion"))):
            msg = "Merci de remplir au moins un des champs parmi 'Types de projet' \
             et 'Autre type de projet'."
            self.add_error("project_types", msg)
            self.add_error("project_types_suggestion", msg)
        return data


class ProjectUpdateForm(forms.ModelForm, DsfrBaseForm):

    name = forms.CharField(
        label="Nom du projet",
        max_length=256,
        required=True,
        help_text=(
            "Donnez un nom explicite : préférez 'végétalisation du quartier des coteaux' \
             à 'quartier des coteaux'"
        ),
    )
    description = RichTextField(
        label="Description de votre projet",
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Entrez ici une description plus précise de votre projet"
            }
        ),
    )
    private_description = RichTextField(
        label="Notes internes de votre projet",
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Informations réservées à vos collaborateurs."}
        ),
    )
    due_date = (
        forms.DateField(
            label="Date d’échéance du projet",
        ),
    )
    project_types = AutocompleteModelMultipleChoiceField(
        label="Types de projet",
        queryset=SynonymList.objects.all(),
        required=False,
        help_text=(
            "Cette information nous aide à identifier les meilleures aides pour votre projet, \
             et à le retrouver plus facilement. Si vous ne trouvez pas le type de projet qui vous \
              correspond, vous pouvez en proposer un nouveau dans le champ 'Autre type de projet'."
        ),
    )
    project_types_suggestion = forms.CharField(
        label="Autre type de projet",
        help_text="Suggérez-nous un autre type de projet.",
        required=False,
    )
    contract_link = forms.ChoiceField(
        label="Appartenance à un plan/programme/contrat",
        choices=Project.CONTRACT_LINK,
        required=False,
    )
    is_public = forms.BooleanField(
        label="Souhaitez-vous rendre ce projet public sur Aides-territoires?",
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "private_description",
            "due_date",
            "project_types",
            "project_types_suggestion",
            "contract_link",
            "is_public",
        ]
        widgets = {
            "due_date": forms.TextInput(
                attrs={"type": "date", "placeholder": "jj/mm/aaaa"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)
        self.fields["contract_link"].choices = [
            ("", "Ce projet appartient-il à un programme?")
        ] + Project.CONTRACT_LINK

    def clean(self):
        data = super().clean()
        if not any((data.get("project_types"), data.get("project_types_suggestion"))):
            msg = "Merci de remplir au moins un des champs parmi 'Types de projet' \
                et 'Autre type de projet'."
            self.add_error("project_types", msg)
            self.add_error("project_types_suggestion", msg)
        return data


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
