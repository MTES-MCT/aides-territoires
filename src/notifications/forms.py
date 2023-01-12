from django import forms

from accounts.models import User
from core.forms.baseform import AidesTerrBaseForm

from notifications.constants import (
    NOTIFICATION_SETTINGS_MODES_LIST,
    NOTIFICATION_SETTINGS_FREQUENCIES_LIST,
)


class NotificationSettingsForm(forms.ModelForm, AidesTerrBaseForm):
    """form to allow user to add/remove a public project to/from its favorite-projects-list."""

    # Notification settings
    notification_aid_team = forms.ChoiceField(
        label="Notifications aides équipe",
        choices=NOTIFICATION_SETTINGS_MODES_LIST,
        help_text="Notifications liées aux aides envoyées à tous les membres de la structure",
    )
    notification_aid_user = forms.ChoiceField(
        label="Notifications aides individuelles",
        choices=NOTIFICATION_SETTINGS_MODES_LIST,
        help_text="Notifications liées aux aides concernant l’utilisateur",
    )
    notification_generic_team = forms.ChoiceField(
        label="Notifications génériques équipe",
        choices=NOTIFICATION_SETTINGS_MODES_LIST,
        help_text="Notifications génériques envoyées à tous les membres de la structure",
    )
    notification_generic_user = forms.ChoiceField(
        label="Notifications génériques individuelles",
        choices=NOTIFICATION_SETTINGS_MODES_LIST,
        help_text="Notifications génériques concernant l’utilisateur",
    )
    notification_email_frequency = forms.ChoiceField(
        label="Fréquence d’envoi des emails de notifications",
        choices=NOTIFICATION_SETTINGS_FREQUENCIES_LIST,
    )

    class Meta:
        model = User
        fields = [
            "notification_aid_team",
            "notification_aid_user",
            "notification_generic_team",
            "notification_generic_user",
            "notification_email_frequency",
        ]
