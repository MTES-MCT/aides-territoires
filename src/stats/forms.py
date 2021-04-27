from django import forms
from django.utils.translation import ugettext_lazy as _

from stats.models import AlertFeedbackEvent


class AlertFeedbackEventForm(forms.ModelForm):
    rate = forms.IntegerField(
        label=_('Rate this alert relevancy from 0 to 5'),
        min_value=0,
        max_value=5,
        widget=forms.TextInput(attrs={
            'type': 'range',
            'min': 1,
            'max': 5,
            'step': 1}))

    feedback = forms.CharField(
        label=_('Leave your feedback of this alert (issues, suggestions…)'),
        min_length=10,
        widget=forms.Textarea(attrs={
            'rows': 3,
        }))

    class Meta:
        model = AlertFeedbackEvent
        fields = ('rate', 'feedback')
