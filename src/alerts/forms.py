from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from alerts.models import Alert
from search.models import SearchPage


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
        help_text=_('How often do you want to receive alerts?'))
    querystring = forms.CharField(widget=forms.HiddenInput, required=False)
    source = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Alert
        fields = ['email', 'title', 'alert_frequency', 'querystring', 'source']

    def clean(self):
        """
        Enforce the unvalidated alert quota.
        For security reasons, there's a max amount of alerts a user can
        create without validating them.
        """
        data = self.cleaned_data

        if 'email' in data:
            email = data['email']
            unvalidated_alerts = Alert.objects \
                .filter(email=email) \
                .filter(validated=False)
            if unvalidated_alerts.count() >= settings.UNVALIDATED_ALERTS_QUOTA:
                msg = _("""
                    You can't create more alerts without validating them.
                    If you don't receive the validation email, please contact
                    us.
                """)
                self.add_error('email', msg)

            all_alerts = Alert.objects.filter(email=email)
            if all_alerts.count() >= settings.MAX_ALERTS_QUOTA:
                msg = _("""
                    You've reached the maximum amount of alerts you can create
                    for your email address.
                """)
                self.add_error('email', msg)

        return data

    def save(self, commit=True):
        """
        If the alert comes from a SearchPage, override the querystring
        with the SearchPage's querystring.
        """
        source = self.cleaned_data.get('source') or 'aides-territoires'
        if source != 'aides-territoires':
            try:
                search_page = SearchPage.objects.get(slug=source)
                self.instance.querystring = search_page.search_querystring
            except SearchPage.DoesNotExist:
                pass
        return super().save(commit=commit)
