from django import forms

from stats.models import AlertFeedbackEvent


class AlertFeedbackEventForm(forms.ModelForm):
    class Meta:
        model = AlertFeedbackEvent
        fields = ('rate', 'feedback')
