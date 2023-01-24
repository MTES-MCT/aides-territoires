from django import forms

from accounts.models import User
from core.forms.baseform import AidesTerrBaseForm

from notifications.constants import NOTIFICATION_SETTINGS_FREQUENCIES_LIST


class NotificationSettingsForm(forms.ModelForm, AidesTerrBaseForm):
    """form to allow user to add/remove a public project to/from its favorite-projects-list."""

    notification_email_frequency = forms.ChoiceField(
        label="Fréquence d’envoi des emails de notifications",
        choices=NOTIFICATION_SETTINGS_FREQUENCIES_LIST,
    )

    class Meta:
        model = User
        fields = [
            "notification_email_frequency",
        ]
