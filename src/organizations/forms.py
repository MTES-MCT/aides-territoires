from django import forms
from core.forms.baseform import AidesTerrBaseForm

from core.forms.fields import AutocompleteModelChoiceField
from core.forms.widgets import SelectWidgetWithDisabledEmptyOption

from geofr.models import Perimeter
from organizations.models import Organization
from organizations.constants import (
    INTERCOMMUNALITY_TYPES,
    ORGANIZATION_TYPES_SINGULAR_GROUPED,
)
from projects.models import Project


class OrganizationTypeWidget(forms.SelectMultiple):
    """Custom widget for the organization_type field."""

    allow_multiple_selected = False

    def create_option(self, *args, **kwargs):
        option_dict = super().create_option(*args, **kwargs)
        if option_dict["value"] == "":
            option_dict["attrs"]["disabled"] = "disabled"
            option_dict["attrs"]["hidden"] = "hidden"
        return option_dict


class OrganizationCreateForm(forms.ModelForm, AidesTerrBaseForm):
    """allow user to create organization."""

    ORGANIZATION_TYPES = [
        ("", "Sélectionnez une valeur")
    ] + ORGANIZATION_TYPES_SINGULAR_GROUPED

    INTERCOMMUNALITY_TYPES_WITH_EMPTY = [
        ("", "Sélectionnez une valeur")
    ] + INTERCOMMUNALITY_TYPES

    name = forms.CharField(
        label="Nom de votre structure",
        required=True,
        help_text="""En fonction des informations saisies précédemment,
        nous pouvons parfois pré-remplir ce champ automatiquement.
        Vous pouvez cependant corriger le nom proposé si besoin.""",
    )
    organization_type = forms.MultipleChoiceField(
        label="Type de votre structure",
        required=True,
        choices=ORGANIZATION_TYPES,
        widget=OrganizationTypeWidget,
    )
    intercommunality_type = forms.ChoiceField(
        label="Type d’intercommunalité",
        required=False,
        choices=INTERCOMMUNALITY_TYPES_WITH_EMPTY,
        widget=SelectWidgetWithDisabledEmptyOption,
    )

    perimeter = AutocompleteModelChoiceField(
        label="Votre territoire", queryset=Perimeter.objects.all(), required=True
    )

    class Meta:
        model = Organization
        fields = ["name", "organization_type", "perimeter"]

    def __init__(self, *args, **kwargs):
        super(OrganizationCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if type(visible.field.widget) in (
                OrganizationTypeWidget,
                SelectWidgetWithDisabledEmptyOption,
            ):
                visible.field.widget.attrs["class"] = "fr-select"


class OrganizationUpdateForm(forms.ModelForm, AidesTerrBaseForm):
    """allow user to update organization's data."""

    ORGANIZATION_TYPES = [
        ("", "Sélectionnez une valeur")
    ] + ORGANIZATION_TYPES_SINGULAR_GROUPED

    INTERCOMMUNALITY_TYPES_WITH_EMPTY = [
        ("", "Sélectionnez une valeur")
    ] + INTERCOMMUNALITY_TYPES

    name = forms.CharField(
        label="Nom de votre structure",
        required=True,
        help_text="""En fonction des informations saisies précédemment,
        nous pouvons parfois pré-remplir ce champ automatiquement.
        Vous pouvez cependant corriger le nom proposé si besoin.""",
    )
    organization_type = forms.MultipleChoiceField(
        label="Type de votre structure",
        required=True,
        choices=ORGANIZATION_TYPES,
        widget=OrganizationTypeWidget,
    )
    intercommunality_type = forms.ChoiceField(
        label="Type d’intercommunalité",
        required=False,
        choices=INTERCOMMUNALITY_TYPES_WITH_EMPTY,
        widget=SelectWidgetWithDisabledEmptyOption,
    )

    address = forms.CharField(label="Adresse postale", required=True)
    city_name = forms.CharField(label="Ville", required=True)
    zip_code = forms.CharField(label="Code postal", required=True)

    siret_code = forms.IntegerField(
        label="Code SIRET", help_text="constitué de 14 chiffres", required=False
    )
    siren_code = forms.IntegerField(
        label="Code SIREN", help_text="constitué de 9 chiffres", required=False
    )
    ape_code = forms.CharField(label="Code APE", required=False)

    perimeter = AutocompleteModelChoiceField(
        label="Votre territoire",
        queryset=Perimeter.objects.all(),
        required=True,
        help_text="Ce champ sera utilisé par défaut pour trouver des aides",
    )

    class Meta:
        model = Organization
        fields = [
            "name",
            "organization_type",
            "address",
            "city_name",
            "zip_code",
            "siren_code",
            "siret_code",
            "ape_code",
            "perimeter",
        ]

    def __init__(self, *args, **kwargs):
        super(OrganizationUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if type(visible.field.widget) in (
                OrganizationTypeWidget,
                SelectWidgetWithDisabledEmptyOption,
            ):
                visible.field.widget.attrs["class"] = "fr-select"


class ProjectToFavoriteForm(forms.ModelForm, AidesTerrBaseForm):
    """form to allow user to add/remove a public project to/from its favorite-projects-list."""

    favorite_projects = AutocompleteModelChoiceField(
        queryset=Project.objects.filter(
            is_public=True, status=Project.STATUS.published
        ),
        required=False,
    )

    class Meta:
        model = Organization
        fields = ["favorite_projects"]
