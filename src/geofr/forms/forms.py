from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelectMultiple
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

# from core.forms import AutocompleteSelectMultiple
from geofr.models import Perimeter


class PerimeterUploadForm(forms.Form):
    city_code_list = forms.FileField(
        label=_('City list (insee codes)'),
        required=True
    )

    def clean_city_code_list(self):
        city_code_list_file = self.cleaned_data['city_code_list']

        # get all city_codes
        city_codes = []
        for line in city_code_list_file:
            try:
                code = line.decode().strip().split(';')[0]
                clean_code = str(code)
                city_codes.append(clean_code)
            except (UnicodeDecodeError, ValueError) as e:
                msg = _('This file seems invalid. \
                        Please double-check its content or contact the \
                        dev team if you feel like it\'s an error. \
                        Here is the original error: {}').format(e)
                raise ValidationError(msg)

        # check these city_codes exist
        perimeters = Perimeter.objects \
            .filter(code__in=city_codes) \
            .filter(scale=Perimeter.TYPES.commune) \
            .values_list('code', flat=True)

        # raise an error if there are unknown city_codes
        missing_city_codes = list(set(city_codes) - set(perimeters))
        if len(missing_city_codes):
            raise ValidationError(mark_safe(
                _('List of missing city codes:') + "<br />"
                + "<br />".join(missing_city_codes))
            )

        return city_code_list_file


class PerimeterCombineForm(forms.Form):
    add_perimeters = forms.ModelMultipleChoiceField(
        label=_('Perimeters to add'),
        queryset=Perimeter.objects.all(),
        widget=AutocompleteSelectMultiple(Perimeter._meta, admin.AdminSite()),
        help_text=_('Select a list of perimeters to combines'))
    rm_perimeters = forms.ModelMultipleChoiceField(
        label=_('Perimeters to substract'),
        required=False,
        queryset=Perimeter.objects.all(),
        widget=AutocompleteSelectMultiple(Perimeter._meta, admin.AdminSite()),
        help_text=_('Those perimeters will be substracted from the '
                    'combined perimeters'))
