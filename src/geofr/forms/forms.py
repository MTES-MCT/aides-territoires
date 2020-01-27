from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelectMultiple
from django.utils.translation import ugettext_lazy as _

# from core.forms import AutocompleteSelectMultiple
from geofr.models import Perimeter


class PerimeterUploadForm(forms.Form):
    city_list = forms.FileField(
        label=_('City list'),
        required=True)


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
