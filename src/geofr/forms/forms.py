from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelectMultiple
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# from core.forms import AutocompleteSelectMultiple
from geofr.models import Perimeter
from geofr.utils import (
    extract_perimeters_from_file,
    query_cities_from_list,
    query_epcis_from_list,
)


class PerimeterUploadForm(forms.Form):
    PERIMETER_TYPE_CHOICES = (
        ("city_code", "Liste de communes (codes insee)"),
        ("epci_name", "Liste d'EPCIs (noms)"),
        ("epci_code", "Liste d'EPCIs (codes)"),
    )

    perimeter_type = forms.ChoiceField(
        label=_("Perimeter type"), required=True, choices=PERIMETER_TYPE_CHOICES
    )
    city_code_list = forms.FileField(
        label="Liste de communes (codes insee)", required=False
    )
    epci_name_list = forms.FileField(label="Liste d'EPCIs (noms)", required=False)
    epci_code_list = forms.FileField(label="Liste d'EPCIs (codes)", required=False)

    def clean(self):
        cleaned_data = super().clean()
        perimeter_type = cleaned_data.get("perimeter_type")
        city_code_list = cleaned_data.get("city_code_list")
        epci_name_list = cleaned_data.get("epci_name_list")
        epci_code_list = cleaned_data.get("epci_code_list")

        if (
            perimeter_type == "city_code"
            and not self.has_error("city_code_list")
            and not city_code_list
        ):
            self.add_error("city_code_list", "Fichier manquant")
        elif (
            perimeter_type == "epci_name"
            and not self.has_error("epci_name_list")
            and not epci_name_list
        ):
            self.add_error("epci_name_list", "Fichier manquant")
        elif (
            perimeter_type == "epci_code"
            and not self.has_error("epci_code_list")
            and not epci_code_list
        ):
            self.add_error("epci_code_list", "Fichier manquant")

    def clean_city_code_list(self):
        city_code_list_file = self.cleaned_data["city_code_list"]

        if city_code_list_file:
            # get all city_codes
            try:
                city_codes = extract_perimeters_from_file(city_code_list_file)
            except Exception as e:
                raise ValidationError(e)

            # check these city_codes exist
            perimeters = query_cities_from_list(city_codes).values_list(
                "code", flat=True
            )

            # raise an error if there are unknown city_codes
            missing_city_codes = list(set(city_codes) - set(perimeters))
            if len(missing_city_codes):
                raise ValidationError(
                    mark_safe(
                        _("List of missing city codes:")
                        + "<br />"
                        + "<br />".join(missing_city_codes)
                    )
                )
        return city_code_list_file

    def clean_epci_name_list(self):
        epci_name_list_file = self.cleaned_data["epci_name_list"]

        if epci_name_list_file:
            # get all epci_names
            try:
                epci_names = extract_perimeters_from_file(epci_name_list_file)
            except Exception as e:
                raise ValidationError(e)

            # check these epci_names exist
            perimeters = query_epcis_from_list(
                epci_names, data_type="names"
            ).values_list("name", flat=True)

            # raise an error if there are unknown epci_names
            missing_epci_names = list(set(epci_names) - set(perimeters))
            if len(missing_epci_names):
                raise ValidationError(
                    mark_safe(
                        "Liste des noms des EPCIs manquants :<br />"
                        + "<br />".join(missing_epci_names)
                    )
                )

        return epci_name_list_file

    def clean_epci_code_list(self):
        epci_code_list_file = self.cleaned_data["epci_code_list"]

        if epci_code_list_file:
            # get all epci_codes
            try:
                epci_codes = extract_perimeters_from_file(epci_code_list_file)
            except Exception as e:
                raise ValidationError(e)

            # check these epci_codes exist
            perimeters = query_epcis_from_list(
                epci_codes, data_type="codes"
            ).values_list("code", flat=True)

            # raise an error if there are unknown epci_codes
            missing_epci_codes = list(set(epci_codes) - set(perimeters))
            if len(missing_epci_codes):
                raise ValidationError(
                    mark_safe(
                        "Liste des codes des EPCIs manquants :<br />"
                        + "<br />".join(missing_epci_codes)
                    )
                )

        return epci_code_list_file


class PerimeterCombineForm(forms.Form):
    add_perimeters = forms.ModelMultipleChoiceField(
        label=_("Perimeters to add"),
        queryset=Perimeter.objects.all(),
        widget=AutocompleteSelectMultiple(
            Perimeter._meta.get_field("contained_in"), admin.AdminSite()
        ),
        help_text=_("Select a list of perimeters to combines"),
    )
    rm_perimeters = forms.ModelMultipleChoiceField(
        label=_("Perimeters to substract"),
        required=False,
        queryset=Perimeter.objects.all(),
        widget=AutocompleteSelectMultiple(
            Perimeter._meta.get_field("contained_in"), admin.AdminSite()
        ),
        help_text=_(
            "Those perimeters will be substracted from the " "combined perimeters"
        ),
    )
