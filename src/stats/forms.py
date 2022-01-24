from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError


class StatSearchForm(forms.Form):

    start_date = forms.DateTimeField(
        label="Date de début",
        required=True,
        widget=forms.TextInput(
            attrs={'type': 'date', 'placeholder': 'jj/mm/aaaa'}))

    end_date = forms.DateTimeField(
        label="Date de fin",
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date', 'placeholder': 'jj/mm/aaaa'}))

    def clean(self):
        """Validation routine (frontend form only)."""

        data = super().clean()

        if data.get('start_date'):
            if data.get('start_date') > timezone.now():
                msg = "la date de début ne peut être dans le futur."
                self.add_error('start_date', msg)
            elif data.get('end_date') > timezone.now():
                msg = "la date de fin ne peut être dans le futur."
                self.add_error('start_date', msg)
            elif data.get('start_date') > data.get('end_date'):
                msg = "Merci de choisir une date de début antérieure à la date de fin."
                self.add_error('start_date', msg)

        return data
