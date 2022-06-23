from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput

from dsfr.forms import DsfrBaseForm


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = "captcha/captcha_field.html"


class ContactForm(DsfrBaseForm):
    """Contact form."""

    SUBJECT_CHOICES = (
        (None, "----"),
        (
            "contact_add",
            "Je veux en savoir plus sur l’ajout de mes aides sur la plateforme",
        ),
        ("contact_com", "Je souhaite communiquer sur Aides-territoires"),
        ("contact_question", "J’ai une question sur mon compte utilisateur"),
        ("contact_blog", "J’ai une question concernant le blog"),
        ("contact_api", "Je souhaite utiliser les données d’Aides-territoires / API"),
        ("contact_tech", "J'ai un problème technique sur le site"),
        ("contact_other", "Autres"),
    )

    first_name = forms.CharField(
        label="Votre prénom",
        widget=forms.TextInput(attrs={"autofocus": "autofocus"}),
        required=False,
    )
    last_name = forms.CharField(label="Votre nom", required=False)
    email = forms.EmailField(label="Votre adresse e-mail", required=True)
    phone = forms.CharField(
        label="Votre numéro de téléphone", max_length=16, required=False
    )
    # honeypot field, not actually used
    website = forms.CharField(
        label="Votre site internet",
        help_text="Merci de laisser ce champ vide",
        required=False,
    )

    organization_and_role = forms.CharField(
        label="Votre structure et fonction",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Exemple: Mairie de Château-Thierry / Chargé de mission habitat"
            }
        ),  # noqa
        required=False,
    )

    subject = forms.ChoiceField(label="Sujet", choices=SUBJECT_CHOICES, required=True)

    message = forms.CharField(
        label="Votre question ou message", widget=forms.Textarea, required=True
    )

    captcha = CaptchaField(
        label="Merci de taper les lettres ci-dessous",
        help_text="Cela nous aide à lutter contre le spam",
        error_messages={"invalid": "Le texte entré ne correspond pas à l’image"},
        widget=CustomCaptchaTextInput,
    )
