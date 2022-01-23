from django import forms

from model_utils import Choices
from core.forms.fields import AutocompleteModelChoiceField

from geofr.models import Perimeter
from organizations.models import Organization


class OrganizationTypeWidget(forms.SelectMultiple):
    """Custom widget for the organization_type field."""

    allow_multiple_selected = False


class OrganizationCreateForm(forms.ModelForm):
    """allow user to create organization."""

    ORGANIZATION_TYPE = Choices(
        ('farmer', 'Agriculteurs'),
        ('association', 'Associations'),
        ('special', "Collectivités d'outre-mer à statuts particuliers"),
        ('commune', 'Communes'),
        ('department', 'Départements'),
        ('private_sector', 'Entreprises privées'),
        ('public_cies', "Entreprises publiques locales (Sem, Spl, SemOp)"),
        ('epci', 'EPCI à fiscalité propre'),
        ('public_org', "Établissements publics (écoles, bibliothèques…) / Services de l'État"),
        ('private_person', 'Particuliers'),
        ('region', 'Régions'),
        ('researcher', 'Recherche'),
    )

    name = forms.CharField(
        label='Nom de votre structure',
        required=True)
    organization_type = forms.MultipleChoiceField(
        label='Vous êtes un/une',
        required=False,
        choices=ORGANIZATION_TYPE,
        widget=OrganizationTypeWidget)

    perimeter = AutocompleteModelChoiceField(
        label='Votre territoire',
        queryset=Perimeter.objects.all(),
        required=True)

    class Meta:
        model = Organization
        fields = ['name', 'organization_type', 'perimeter']


class OrganizationUpdateForm(forms.ModelForm):
    """allow user to update organization's data."""

    name = forms.CharField(
        label='Nom de la structure',
        required=True)
    address = forms.CharField(
        label='Adresse postale',
        required=True)
    city_name = forms.CharField(
        label='Ville',
        required=True)
    zip_code = forms.CharField(
        label='Code postal',
        required=True)

    siret_code = forms.IntegerField(
        label='Code SIRET',
        help_text='constitué de 14 chiffres',
        required=False)
    siren_code = forms.IntegerField(
        label='Code SIREN',
        help_text='constitué de 9 chiffres',
        required=False)
    ape_code = forms.CharField(
        label='Code APE',
        required=False)

    perimeter = AutocompleteModelChoiceField(
        label='Votre territoire',
        queryset=Perimeter.objects.all(),
        required=True,
        help_text="Ce champ sera utilisé par défaut pour trouver des aides")

    class Meta:
        model = Organization
        fields = [
            'name', 'address', 'city_name', 'zip_code',
            'siren_code', 'siret_code', 'ape_code', 'perimeter']

    def __init__(self, *args, **kwargs):
        super(OrganizationUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'fr-input'
