from django import forms
from django.utils.translation import ugettext_lazy as _

from geofr.forms.fields import PerimeterChoiceField


AUDIANCES = [
    (_('A collectivity'), (
        ('commune', _('Commune')),
        ('department', _('Department')),
        ('region', _('Region')),
    )),
    (_('An other beneficiary'), (
        ('public_org', _('Public organizations')),
        ('association', _('Associations')),
    ))
]


class AudianceWidget(forms.widgets.ChoiceWidget):
    """Custom widget for the audiance search step."""

    allow_multiple_selected = False
    template_name = 'search/forms/widgets/audiance_widget.html'


class AudianceSearchForm(forms.Form):
    targeted_audiances = forms.ChoiceField(
        label=_('Your are seeking aids for…'),
        required=False,
        choices=AUDIANCES,
        widget=AudianceWidget)


class PerimeterSearchForm(forms.Form):
    targeted_audiances = forms.ChoiceField(
        choices=AUDIANCES,
        widget=forms.widgets.HiddenInput)
    perimeter = PerimeterChoiceField(
        label=_('Your territory'),
        required=False)
