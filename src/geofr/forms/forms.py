from django import forms
from django.utils.translation import ugettext_lazy as _


class PerimeterUploadForm(forms.Form):
    city_list = forms.FileField(
        label=_('City list'),
        required=True)
