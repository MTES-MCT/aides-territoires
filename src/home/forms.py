from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    """Contact form."""

    SUBJECT_CHOICES = (
        (None, '----'),
        ('contact_tech', 'J\'ai un problème technique sur le site'),
        ('contact_add', 'Je veux en savoir plus sur l\'ajout de mes aides sur la plateforme'),  # noqa
        ('contact_com', 'Je souhaite communiquer sur Aides-territoires'),
        ('contact_question', 'J\'ai une question par rapport à une aide ou mon projet'),  # noqa
        ('contact_other', 'Autres')
    )

    first_name = forms.CharField(
        label=_('Your first name'),
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),
        required=False)
    last_name = forms.CharField(
        label=_('Your last name'),
        required=False)
    email = forms.EmailField(
        label=_('Your email address'),
        required=True)
    phone = forms.CharField(
        label=_('Your phone number'),
        max_length=16,
        required=False)
    organization_and_role = forms.CharField(
        label='Votre structure et fonction',
        widget=forms.TextInput(
            attrs={'placeholder': 'Mairie de Château-Thierry / Chargé de mission habitat'}),  # noqa
        required=False)

    subject = forms.ChoiceField(
        label='Sujet',
        choices=SUBJECT_CHOICES,
        required=True)

    message = forms.CharField(
        label='Votre question ou message',
        widget=forms.Textarea,
        required=True)
