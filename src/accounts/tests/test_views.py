"""Test user login views."""

import pytest
import re
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


def test_login_email_token_works(client, user, mailoutbox):
    login_url = reverse('login_request')
    res = client.post(login_url, {'email': user.email})
    assert not res.wsgi_request.user.is_authenticated

    mail_body = mailoutbox[0].body
    re_match = re.search(r'^https://[\w.-]*(.*)$', mail_body, re.MULTILINE)
    url = re_match.group(1)
    res = client.get(url, follow=True)
    assert res.status_code == 200
    assert 'You are now logged in' in res.content.decode()
    assert res.wsgi_request.user.is_authenticated


def test_login_with_wrong_token(client, user, mailoutbox):
    login_url = reverse('login_request')
    res = client.post(login_url, {'email': user.email})
    assert not res.wsgi_request.user.is_authenticated

    mail_body = mailoutbox[0].body
    re_match = re.search(
        r'^https://[\w.-]*/accounts/login/(.*)/(.*)/$',
        mail_body,
        re.MULTILINE)
    uidb64 = re_match.group(1)
    url = reverse('login', args=[uidb64, 'wrong_token'])
    res = client.get(url, follow=True)
    assert res.status_code == 200
    assert 'Something went wrong' in res.content.decode()
    assert not res.wsgi_request.user.is_authenticated


def test_login_with_wrong_user_id(client, user, mailoutbox):
    login_url = reverse('login_request')
    res = client.post(login_url, {'email': user.email})
    assert not res.wsgi_request.user.is_authenticated

    mail_body = mailoutbox[0].body
    re_match = re.search(
        r'^https://[\w.-]*/accounts/login/(.*)/(.*)/$',
        mail_body,
        re.MULTILINE)
    token = re_match.group(2)
    url = reverse('login', args=['wrong_uid', token])
    res = client.get(url, follow=True)
    assert res.status_code == 200
    assert 'Something went wrong' in res.content.decode()
    assert not res.wsgi_request.user.is_authenticated
