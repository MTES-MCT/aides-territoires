from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelectMultiple
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# from core.forms import AutocompleteSelectMultiple
from geofr.models import Perimeter
from geofr.utils import (extract_perimeters_from_file,
                         query_cities_from_list, query_epcis_from_list)


class PerimeterUploadForm(forms.Form):
    PERIMETER_TYPE_CHOICES = (
        ('city_code', _('City list (insee codes)')),
        ('epci_name', _('EPCI list (names)')),
    )

    perimeter_type = forms.ChoiceField(
        label=_('Perimeter type'),
        required=True,
        choices=PERIMETER_TYPE_CHOICES
    )
    city_code_list = forms.FileField(
        label=_('City list (insee codes)'),
        required=False
    )
    epci_name_list = forms.FileField(
        label=('EPCI list (names)'),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        perimeter_type = cleaned_data.get("perimeter_type")
        city_code_list = cleaned_data.get("city_code_list")
        epci_name_list = cleaned_data.get("epci_name_list")

        if perimeter_type == 'city_code' and not self.has_error('city_code_list') and not city_code_list:  # noqa
            self.add_error('city_code_list', 'File missing')
        elif perimeter_type == 'epci_name' and not self.has_error('epci_name_list') and not epci_name_list:  # noqa
            self.add_error('epci_name_list', 'File missing')

    def clean_city_code_list(self):
        city_code_list_file = self.cleaned_data['city_code_list']

        if city_code_list_file:
            # get all city_codes
            try:
                city_codes = extract_perimeters_from_file(city_code_list_file)
            except Exception as e:
                raise ValidationError(e)

            # check these city_codes exist
            perimeters = query_cities_from_list(city_codes) \
                .values_list('code', flat=True)

            # raise an error if there are unknown city_codes
            missing_city_codes = list(set(city_codes) - set(perimeters))
            if len(missing_city_codes):
                raise ValidationError(mark_safe(
                    _('List of missing city codes:') + "<br />"
                    + "<br />".join(missing_city_codes))
                )
        return city_code_list_file

    def clean_epci_name_list(self):
        epci_name_list_file = self.cleaned_data['epci_name_list']

        if epci_name_list_file:
            # get all epci_names
            try:
                epci_names = extract_perimeters_from_file(epci_name_list_file)
            except Exception as e:
                raise ValidationError(e)

            # check these epci_names exist
            perimeters = query_epcis_from_list(epci_names) \
                .values_list('name', flat=True)

            # raise an error if there are unknown epci_names
            missing_epci_names = list(set(epci_names) - set(perimeters))
            if len(missing_epci_names):
                raise ValidationError(mark_safe(
                    _('List of missing EPCI names:') + "<br />"
                    + "<br />".join(missing_epci_names))
                )

        return epci_name_list_file


class PerimeterCombineForm(forms.Form):
    add_perimeters = forms.ModelMultipleChoiceField(
        label=_('Perimeters to add'),
        queryset=Perimeter.objects.all(),
        widget=AutocompleteSelectMultiple(
            Perimeter._meta.get_field('contained_in'), admin.AdminSite()),
        help_text=_('Select a list of perimeters to combines'))
    rm_perimeters = forms.ModelMultipleChoiceField(
        label=_('Perimeters to substract'),
        required=False,
        queryset=Perimeter.objects.all(),
        widget=AutocompleteSelectMultiple(
            Perimeter._meta.get_field('contained_in'), admin.AdminSite()),
        help_text=_(
            'Those perimeters will be substracted from the '
            'combined perimeters'))
