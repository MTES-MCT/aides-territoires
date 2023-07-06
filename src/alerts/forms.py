from django import forms
from django.conf import settings

from alerts.models import Alert
from core.forms.baseform import AidesTerrBaseForm


class AlertForm(forms.ModelForm, AidesTerrBaseForm):
    email = forms.EmailField(
        label="Votre adresse e-mail",
        help_text="Nous enverrons un e-mail pour confirmer votre adresse",
        required=True,
        error_messages={
            "invalid": "Saisissez une adresse e-mail valide, par exemple prenom.nom@domaine.fr."
        },
    )
    title = forms.CharField(
        label="Donnez un nom à votre alerte", required=True, max_length=250
    )
    alert_frequency = forms.ChoiceField(
        label="Fréquence de l’alerte",
        choices=Alert.FREQUENCIES,
        help_text="À quelle fréquence souhaitez-vous recevoir les nouveaux résultats ?",
    )
    querystring = forms.CharField(widget=forms.HiddenInput, required=False)
    source = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Alert
        fields = ["email", "title", "alert_frequency", "querystring", "source"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"autocomplete": "email"})

    def clean(self):
        """
        Enforce the unvalidated alert quota.
        For security reasons, there's a max amount of alerts a user can
        create without validating them.
        """
        data = self.cleaned_data

        if "email" in data:
            email = data["email"]
            unvalidated_alerts = Alert.objects.filter(email=email).filter(
                validated=False
            )
            if unvalidated_alerts.count() >= settings.UNVALIDATED_ALERTS_QUOTA:
                msg = """
                Vous ne pouvez pas créer de nouvelles alertes avant de valider celles existantes.
                Si vous ne recevez pas les e-mails de validation, merci de nous contacter.
                """

                self.add_error("email", msg)

            all_alerts = Alert.objects.filter(email=email)
            if all_alerts.count() >= settings.MAX_ALERTS_QUOTA:
                msg = """
                Vous avez atteint le nombre maximum d’alertes qu’il est possible de créer
                pour une seule adresse e-mail.
                """

                self.add_error("email", msg)

        return data


class DeleteAlertForm(AidesTerrBaseForm):
    token = forms.UUIDField(widget=forms.HiddenInput(), required=True)
