from django import forms
from django.utils.translation import ugettext_lazy as _

from alerts.models import Alert


class AlertForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('Your email address'),
        help_text=_('We will send an email to confirm your address'),
        required=True)
    title = forms.CharField(
        label=_('Give a name to your alert'),
        required=True,
        max_length=250)
    alert_frequency = forms.ChoiceField(
        label=_('Alert frequency'),
        choices=Alert.FREQUENCIES,
        help_text=_('How often to you want to receive alerts?'))
    querystring = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Alert
        fields = ['email', 'title', 'alert_frequency', 'querystring']
