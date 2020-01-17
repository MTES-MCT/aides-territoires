from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

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

    def clean(self):
        """Enforce the unvalidated alert quota.

        For security reasons, there's a max amount of alerts a user can
        create without validating them.
        """
        data = self.cleaned_data

        if 'email' in data:
            unvalidated_alerts = Alert.objects \
                .filter(email=data['email']) \
                .filter(validated=False)
            if unvalidated_alerts.count() >= settings.UNVALIDATED_ALERTS_QUOTA:
                msg = _("""
                    You can't create more alerts without validating them.
                    If you don't receive the validation email, please contact
                    us.
                """)
                self.add_error('email', msg)

        return data
