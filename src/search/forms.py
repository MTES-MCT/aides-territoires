from django import forms
from django.utils.translation import ugettext_lazy as _


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
    allow_multiple_selected = True
    template_name = 'search/forms/widgets/audiance_widget.html'


class AudianceSearchForm(forms.Form):
    targeted_audiances = forms.MultipleChoiceField(
        label=_('Your are seeking aids for…'),
        required=False,
        choices=AUDIANCES,
        widget=AudianceWidget)
