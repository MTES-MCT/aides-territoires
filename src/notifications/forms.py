from django import forms

from accounts.models import User
from core.forms.baseform import AidesTerrBaseForm

from notifications.constants import NOTIFICATION_SETTING_LIST


class NotificationSettingsForm(forms.ModelForm, AidesTerrBaseForm):
    """form to allow user to add/remove a public project to/from its favorite-projects-list."""

    # Notification settings
    notification_aid_team = forms.ChoiceField(
        label="Notifications aides équipe",
        choices=NOTIFICATION_SETTING_LIST,
        help_text="Notifications liées aux aides envoyées à tous les membres de la structure",
    )
    notification_aid_user = forms.ChoiceField(
        label="Notifications aides individuelles",
        choices=NOTIFICATION_SETTING_LIST,
        help_text="Notifications liées aux aides concernant l’utilisateur",
    )
    notification_internal_team = forms.ChoiceField(
        label="Notifications internes équipe",
        choices=NOTIFICATION_SETTING_LIST,
        help_text="Notifications internes envoyées à tous les membres de la structure",
    )
    notification_internal_user = forms.ChoiceField(
        label="Notifications interne individuelles",
        choices=NOTIFICATION_SETTING_LIST,
        help_text="Notifications internes concernant l’utilisateur",
    )

    class Meta:
        model = User
        fields = [
            "notification_aid_team",
            "notification_aid_user",
            "notification_internal_team",
            "notification_internal_user",
        ]
