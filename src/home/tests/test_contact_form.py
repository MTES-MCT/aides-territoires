from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from home.forms import ContactForm
from home.tasks import send_contact_form_email
from stats.models import ContactFormSendEvent


class ContactFormTestCase(TestCase):

    sample_data = {
        "first_name": "Gustave",
        "last_name": "Labarbe",
        "email": "mairie.champignac@cc-cambrousse.fr",
        "phone": "+33612345789",
        "website": "",
        "organization_and_role": "Champignac-en-Cambrousse / Monsieur le Maire",
        "subject": "contact_com",
        "message": """
        Ce chef-d'œuvre en pied, dû à un cerveau de chez nous marchant main dans la
        main avec le cœur de notre belle agglomération, contient à tout jamais dans
        le vide de ses flancs la plénitude du génie champignacien.
        """,
    }

    sample_data_2 = {
        "first_name": "Gustave",
        "last_name": "Labarbe",
        "email": "mairie.champignac@cc-cambrousse.fr",
        "phone": "+33612345789",
        "website": "",
        "organization_and_role": "Champignac-en-Cambrousse / Monsieur le Maire",
        "subject": "contact_com",
        "message": """
        Ce chef-d'œuvre en pied, dû à un cerveau de chez nous marchant main dans la
        main avec le cœur de notre belle agglomération, contient à tout jamais dans
        le vide de ses flancs la plénitude du génie champignacien.
        """,
        "id": "140314043890128",
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_contact_form_valid(self):
        form = ContactForm(data=self.sample_data)

        self.assertTrue(form.is_valid())

    def test_contact_form_valid_even_with_honeypot(self):
        sample_data = self.sample_data
        sample_data["website"] = "https://example.com/"
        form = ContactForm(data=sample_data)

        self.assertTrue(form.is_valid())

    @patch.object(send_contact_form_email, "delay")
    def test_contact_form_sends_message(self, *args):
        url = reverse("contact")
        response = self.client.post(url, data=self.sample_data, follow=True)

        send_contact_form_email.delay.assert_called_once()

        self.assertContains(
            response,
            "Votre message a bien été envoyé, merci !",
            html=True,
        )

    @patch.object(send_contact_form_email, "delay")
    def test_contactformsendevent_is_created_if_honeypot_is_empty(self, *args):
        url = reverse("contact")
        response = self.client.post(url, data=self.sample_data_2, follow=True)

        send_contact_form_email.delay.assert_called_once()

        self.assertContains(
            response,
            "Votre message a bien été envoyé, merci !",
            html=True,
        )
        assert ContactFormSendEvent.objects.count() == 1

    @patch.object(send_contact_form_email, "delay")
    def test_contact_form_silently_fails_if_honeypot_is_filled(self, *args):
        sample_data = self.sample_data
        sample_data["website"] = "https://example.com/"

        url = reverse("contact")
        response = self.client.post(url, data=sample_data, follow=True)

        send_contact_form_email.delay.assert_not_called()

        self.assertContains(
            response,
            "Votre message a bien été envoyé, merci !",
            html=True,
        )

    @patch.object(send_contact_form_email, "delay")
    def test_contactformsendevent_is_not_created_if_honeypot_is_filled(self, *args):
        sample_data = self.sample_data
        sample_data["website"] = "https://example.com/"

        url = reverse("contact")
        self.client.post(url, data=sample_data, follow=True)
        assert ContactFormSendEvent.objects.count() == 0
