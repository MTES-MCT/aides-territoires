import re
from django import forms
from django.template.defaultfilters import filesizeformat

from core.forms.baseform import AidesTerrBaseForm
from core.utils import remove_accents

from projects.constants import EXPORT_FORMAT_CHOICES
from core.forms import (
    AutocompleteModelMultipleChoiceField,
    RichTextField,
    AutocompleteModelChoiceField,
)

from projects.models import Project
from organizations.models import Organization
from keywords.models import SynonymList
from geofr.models import Perimeter
from geofr.utils import get_all_related_perimeters
from organizations.constants import ORGANIZATION_TYPE_CHOICES_COMMUNES_OR_EPCI


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = "custom_clearable_file_input.html"


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
    image = forms.FileField(
        label="Ajouter une image représentant votre projet",
        help_text="""Taille maximale : 2 Mio. Formats supportés : jpeg, jpg, png.
            Choisissez de préférence une image au format 1920x1080px.""",
        required=False,
        widget=CustomClearableFileInput(),
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
            "image",
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

    def clean_image(self):
        if self.cleaned_data["image"]:
            image = self.cleaned_data["image"]
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    f"Merci de choisir une image dont le poids est inférieur à 2 Mio. \
                     Le poids de l'image actuellement choisie est de {filesizeformat(image.size)}"
                )
            return image


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
    image = forms.FileField(
        label="Ajouter une image représentant votre projet",
        help_text="""Taille maximale : 2 Mio. Formats supportés : jpeg, jpg, png.
            Choisissez de préférence une image au format 1920x1080px.""",
        required=False,
        widget=CustomClearableFileInput(attrs={"multiple": True}),
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
            "image",
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

    def clean_image(self):
        if self.cleaned_data["image"]:
            image = self.cleaned_data["image"]
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    f"Merci de choisir une image dont le poids est inférieur à 2 Mio. \
                     Le poids de l'image actuellement choisie est de {filesizeformat(image.size)}"
                )
            return image


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


class ProjectSearchForm(AidesTerrBaseForm):
    """Main form for search engine."""

    step = forms.ChoiceField(
        label="Avancement du projet",
        required=False,
        choices=Project.PROJECT_STEPS,
    )

    contract_link = forms.ChoiceField(
        label="Appartenance à un plan",
        required=False,
        choices=Project.CONTRACT_LINK,
    )

    project_types = AutocompleteModelMultipleChoiceField(
        label="Types de projet",
        queryset=SynonymList.objects.all(),
        required=False,
    )

    organization = forms.ChoiceField(
        label="Type de porteur de projet",
        required=False,
        choices=ORGANIZATION_TYPE_CHOICES_COMMUNES_OR_EPCI,
    )

    project_perimeter = AutocompleteModelChoiceField(
        queryset=Perimeter.objects.all(), label="Territoire du projet", required=False
    )

    def __init__(self, *args, **kwargs):
        super(ProjectSearchForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name == "contract_link":
                field = self.fields.get("contract_link")
                field.choices.insert(0, ("", "Tous les plans"))
                field.widget.choices = field.choices
            elif field_name == "step":
                field = self.fields.get("step")
                field.choices.insert(0, ("", "Toutes les étapes"))
                field.widget.choices = field.choices
            elif field_name == "organization":
                field = self.fields.get("organization")
                field.choices.insert(0, ("", "Toutes les structures"))
                field.widget.choices = field.choices

    def clean_zipcode(self):
        zipcode = self.cleaned_data["zipcode"]
        if zipcode and re.match(r"\d{5}", zipcode) is None:
            msg = "Ce code postal semble invalide."
            raise forms.ValidationError(msg)

        return zipcode

    def filter_queryset(self, qs=None):
        """Filter querysets depending of input data."""

        # Populate cleaned_data
        if not hasattr(self, "cleaned_data"):
            self.full_clean()

        step = self.cleaned_data.get("step", None)
        if step:
            qs = qs.filter(step=step)

        contract_link = self.cleaned_data.get("contract_link", None)
        if contract_link:
            qs = qs.filter(contract_link=contract_link)

        project_perimeter = self.cleaned_data.get("project_perimeter", None)
        if project_perimeter:
            qs = self.perimeter_filter(qs, project_perimeter)

        project_types = self.cleaned_data.get("project_types", None)
        if project_types:
            qs = qs.filter(project_types__in=project_types)

        organization = self.cleaned_data.get("organization", None)
        if organization:
            qs = qs.filter(organizations__organization_type=[organization])

        return qs

    def perimeter_filter(self, qs, search_perimeter):
        """Filter queryset depending on the given perimeter.

        When we search for a given perimeter, we must return all projects:
         - where the perimeter is wider and contains the searched perimeter ;
         - where the perimeter is smaller and contained by the search
         perimeter ;

        E.g if we search for projects in "Hérault (department), we must display all
        aids that are applicable to:

         - Hérault ;
         - Occitanie ;
         - France ;
         - Europe ;
         - M3M (and all other epcis in Hérault) ;
         - Montpellier (and all other communes in Hérault) ;
        """
        perimeter_ids = get_all_related_perimeters(search_perimeter.id, values=["id"])
        qs = qs.filter(organizations__perimeter__in=perimeter_ids)
        return qs


class ValidatedProjectSearchForm(AidesTerrBaseForm):
    """Specific form for validated projects search engine."""

    name = forms.CharField(
        label="Votre projet",
        required=False,
    )

    project_perimeter = AutocompleteModelChoiceField(
        queryset=Perimeter.objects.all(), label="Périmètre", required=True
    )

    def clean_zipcode(self):
        zipcode = self.cleaned_data["zipcode"]
        if zipcode and re.match(r"\d{5}", zipcode) is None:
            msg = "Ce code postal semble invalide."
            raise forms.ValidationError(msg)

        return zipcode

    def filter_queryset(self, qs=None):
        """Filter querysets depending of input data."""

        # Populate cleaned_data
        if not hasattr(self, "cleaned_data"):
            self.full_clean()

        project_perimeter = self.cleaned_data.get("project_perimeter", None)
        if project_perimeter:
            qs = self.perimeter_filter(qs, project_perimeter)

        name = self.cleaned_data.get("name", None)
        if name:
            name_unaccented = remove_accents(name)
            qs = qs.filter(project_name__icontains=name_unaccented)

        return qs

    def perimeter_filter(self, qs, search_perimeter):
        """Filter queryset depending on the given perimeter.

        When we search for a given perimeter, we must return all projects:
         - where the perimeter is wider and contains the searched perimeter ;
         - where the perimeter is smaller and contained by the search
         perimeter ;

        E.g if we search for projects in "Hérault (department), we must display all
        aids that are applicable to:

         - Hérault ;
         - Occitanie ;
         - France ;
         - Europe ;
         - M3M (and all other epcis in Hérault) ;
         - Montpellier (and all other communes in Hérault) ;
        """
        perimeter_ids = get_all_related_perimeters(search_perimeter.id, values=["id"])
        qs = qs.filter(organization__perimeter__in=perimeter_ids)
        return qs


class ValidatedProjectImportForm(forms.Form):
    validated_projects_list = forms.FileField(
        label="Liste des projets subventionnés", required=True
    )
