"""Test user login views."""

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_login_view_is_for_anonymous_only(client, user):
    """Authenticated users cannot login again, duh!"""

    client.force_login(user)
    login_url = reverse('login_request')
    res = client.get(login_url)
    assert res.status_code == 302


def test_login_view_is_accessible_for_anonymous_users(client):
    login_url = reverse('login_request')
    res = client.get(login_url)
    assert res.status_code == 200


def test_login_with_incorrect_email_does_not_send_any_email(
        client, user, mailoutbox):
    login_url = reverse('login_request')
    res = client.post(login_url, {'email': 'fake@email.com'})
    assert res.status_code == 302
    assert len(mailoutbox) == 0


def test_login_with_existing_email_does_send_an_email(
        client, user, mailoutbox):
    login_url = reverse('login_request')
    res = client.post(login_url, {'email': user.email})
    assert res.status_code == 302
    assert len(mailoutbox) == 1

    mail = mailoutbox[0]
    assert mail.subject == 'Connexion à Aides-Territoires'