from django import forms

from core.forms.baseform import AidesTerrBaseForm

from projects.constants import EXPORT_FORMAT_CHOICES
from core.forms import (
    AutocompleteModelMultipleChoiceField,
    RichTextField,
)

from projects.models import Project
from organizations.models import Organization
from keywords.models import SynonymList


class ProjectCreateForm(forms.ModelForm, AidesTerrBaseForm):
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
        help_text="Ces informations restent internes à votre organisation \
             même si vous rendez votre projet public.",
    )
    step = forms.ChoiceField(
        label="État d’avancement du projet",
        choices=Project.PROJECT_STEPS,
        required=True,
    )
    budget = forms.IntegerField(
        label="Budget prévisonnel",
        help_text="Montant du budget prévisionnel en euros",
        required=False,
    )
    organizations = forms.ModelMultipleChoiceField(
        label="Créateur du projet", queryset=Organization.objects.all(), required=False
    )
    other_project_owner = forms.CharField(
        label="Autre maître d’ouvrage",
        required=False,
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
            "step",
            "budget",
            "organizations",
            "other_project_owner",
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
        self.fields["step"].choices = [
            ("", "À quel stade est ce projet?")
        ] + Project.PROJECT_STEPS

    def clean(self):
        data = super().clean()
        if not any((data.get("project_types"), data.get("project_types_suggestion"))):
            msg = "Merci de remplir au moins un des champs parmi 'Types de projet' \
            et 'Autre type de projet'."
            self.add_error("project_types", msg)
            self.add_error("project_types_suggestion", msg)
        return data


class ProjectUpdateForm(forms.ModelForm, AidesTerrBaseForm):

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
    step = forms.ChoiceField(
        label="État d’avancement du projet",
        choices=Project.PROJECT_STEPS,
        required=True,
    )
    budget = forms.IntegerField(
        label="Budget prévisonnel",
        help_text="Montant du budget prévisionnel en euros",
        required=False,
    )
    other_project_owner = forms.CharField(
        label="Autre maître d’ouvrage",
        required=False,
    )
    private_description = RichTextField(
        label="Notes internes de votre projet",
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Informations réservées à vos collaborateurs."}
        ),
        help_text="Ces informations restent internes à votre organisation \
             même si vous rendez votre projet public.",
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
            "step",
            "budget",
            "other_project_owner",
            "project_types",
            "project_types_suggestion",
            "contract_link",
            "is_public",
        ]

    def __init__(self, *args, **kwargs):
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)
        self.fields["contract_link"].choices = [
            ("", "Ce projet appartient-il à un programme?")
        ] + Project.CONTRACT_LINK
        self.fields["step"].choices = [
            ("", "À quel stade est ce projet?")
        ] + Project.PROJECT_STEPS

    def clean(self):
        data = super().clean()
        if not any((data.get("project_types"), data.get("project_types_suggestion"))):
            msg = "Merci de remplir au moins un des champs parmi 'Types de projet' \
                et 'Autre type de projet'."
            self.add_error("project_types", msg)
            self.add_error("project_types_suggestion", msg)
            self.fields["project_types"].widget.attrs.update({"autofocus": True})

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
