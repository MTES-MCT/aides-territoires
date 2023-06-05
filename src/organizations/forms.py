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
        label="Votre territoire",
        queryset=Perimeter.objects.all(),
        required=True,
        help_text="""Ce champ sera utilisé par défaut pour trouver des aides.
                Tous les périmètres géographiques sont disponibles :
        CA, CU, CC, pays, parc, etc. Contactez-nous si vous ne trouvez pas vôtre.""",
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
        help_text="""Ce champ sera utilisé par défaut pour trouver des aides.
                Tous les périmètres géographiques sont disponibles :
        CA, CU, CC, pays, parc, etc. Contactez-nous si vous ne trouvez pas vôtre.""",
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
            "intercommunality_type",
        ]

    def __init__(self, *args, **kwargs):
        super(OrganizationUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if type(visible.field.widget) in (
                OrganizationTypeWidget,
                SelectWidgetWithDisabledEmptyOption,
            ):
                visible.field.widget.attrs["class"] = "fr-select"


class OrganizationDataForm(forms.ModelForm, AidesTerrBaseForm):
    """allow user to submit organization's infrastructure's data."""

    inhabitants_number = forms.DecimalField(
        label="Habitants",
        required=False,
        min_value=0,
    )
    voters_number = forms.DecimalField(
        label="Votants",
        required=False,
        min_value=0,
    )
    corporates_number = forms.DecimalField(
        label="Entreprise",
        required=False,
        min_value=0,
    )
    shops_number = forms.DecimalField(
        label="Commerce",
        required=False,
        min_value=0,
    )
    associations_number = forms.DecimalField(
        label="Association",
        required=False,
        min_value=0,
    )
    municipal_roads = forms.DecimalField(
        label="Routes communales (kms)",
        required=False,
        min_value=0,
    )
    departmental_roads = forms.DecimalField(
        label="Routes départementales (kms)",
        required=False,
        min_value=0,
    )
    tram_roads = forms.DecimalField(
        label="Tramway (kms)",
        required=False,
        min_value=0,
    )
    lamppost_number = forms.DecimalField(
        label="Lampadaires",
        required=False,
        min_value=0,
    )
    bridge_number = forms.DecimalField(
        label="Ponts",
        required=False,
        min_value=0,
    )
    library_number = forms.DecimalField(
        label="Bibliothèque",
        required=False,
        min_value=0,
    )
    medialibrary_number = forms.DecimalField(
        label="Médiathèque",
        required=False,
        min_value=0,
    )
    theater_number = forms.DecimalField(
        label="Théâtre",
        required=False,
        min_value=0,
    )
    cinema_number = forms.DecimalField(
        label="Cinéma",
        required=False,
        min_value=0,
    )
    museum_number = forms.DecimalField(
        label="Musée",
        required=False,
        min_value=0,
    )
    nursery_number = forms.DecimalField(
        label="Crèche",
        required=False,
        min_value=0,
    )
    kindergarten_number = forms.DecimalField(
        label="École maternelle",
        required=False,
        min_value=0,
    )
    primary_school_number = forms.DecimalField(
        label="École élémentaire",
        required=False,
        min_value=0,
    )
    rec_center_number = forms.DecimalField(
        label="Centre de loisirs",
        required=False,
        min_value=0,
    )
    middle_school_number = forms.DecimalField(
        label="Collège",
        required=False,
        min_value=0,
    )
    high_school_number = forms.DecimalField(
        label="Lycée",
        required=False,
        min_value=0,
    )
    university_number = forms.DecimalField(
        label="Université",
        required=False,
        min_value=0,
    )
    tennis_court_number = forms.DecimalField(
        label="Court de tennis",
        required=False,
        min_value=0,
    )
    football_field_number = forms.DecimalField(
        label="Terrain de football",
        required=False,
        min_value=0,
    )
    running_track_number = forms.DecimalField(
        label="Piste d'athlétisme",
        required=False,
        min_value=0,
    )
    other_outside_structure_number = forms.DecimalField(
        label="Structure extérieure autre",
        required=False,
        min_value=0,
    )
    covered_sporting_complex_number = forms.DecimalField(
        label="Complexe sportif couvert",
        required=False,
        min_value=0,
    )
    swimming_pool_number = forms.DecimalField(
        label="Piscine",
        required=False,
        min_value=0,
    )
    place_of_worship_number = forms.DecimalField(
        label="Lieux de cultes",
        required=False,
        min_value=0,
    )
    cemetery_number = forms.DecimalField(
        label="Cimetière",
        required=False,
        min_value=0,
    )
    protected_monument_number = forms.DecimalField(
        label="Monument classé",
        required=False,
        min_value=0,
    )
    forest_number = forms.DecimalField(
        label="Forêt (en hectares)",
        required=False,
        min_value=0,
    )

    class Meta:
        model = Organization
        fields = [
            "inhabitants_number",
            "voters_number",
            "corporates_number",
            "shops_number",
            "associations_number",
            "municipal_roads",
            "departmental_roads",
            "tram_roads",
            "lamppost_number",
            "bridge_number",
            "library_number",
            "medialibrary_number",
            "theater_number",
            "cinema_number",
            "museum_number",
            "nursery_number",
            "kindergarten_number",
            "primary_school_number",
            "rec_center_number",
            "middle_school_number",
            "high_school_number",
            "university_number",
            "tennis_court_number",
            "football_field_number",
            "running_track_number",
            "other_outside_structure_number",
            "covered_sporting_complex_number",
            "swimming_pool_number",
            "place_of_worship_number",
            "cemetery_number",
            "protected_monument_number",
            "forest_number",
        ]


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
