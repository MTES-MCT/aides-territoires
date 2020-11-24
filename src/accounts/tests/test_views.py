"""Test user login views."""

import pytest
import re
from django.urls import reverse
from django.contrib.auth import authenticate

from accounts.models import User

pytestmark = pytest.mark.django_db


def test_login_view_is_for_anonymous_only(client, user):
    """Authenticated users cannot login again, duh!"""

    client.force_login(user)
    login_url = reverse('login')
    res = client.get(login_url)
    assert res.status_code == 302


def test_login_view_is_accessible_for_anonymous_users(client):
    login_url = reverse('login')
    res = client.get(login_url)
    assert res.status_code == 200


def test_login_is_case_insensitive(client, user):
    user.email = 'test@test.com'
    user.set_password('pass')
    user.save()

    login_url = reverse('login')
    res = client.get(login_url)
    assert res.status_code == 200
    assert not res.wsgi_request.user.is_authenticated

    res = client.post(
        login_url,
        {'username': 'TEST@TEST.com', 'password': 'pass'})
    assert res.status_code == 302
    assert res.wsgi_request.user.is_authenticated


def test_password_reset_with_existing_email_does_send_an_email(
        client, user, mailoutbox):
    login_url = reverse('password_reset')
    res = client.post(login_url, {'username': user.email})
    assert res.status_code == 302
    assert len(mailoutbox) == 1

    mail = mailoutbox[0]
    assert mail.subject == 'Connexion à Aides-territoires'


def test_login_email_token_works(client, user, mailoutbox):
    login_url = reverse('password_reset')
    res = client.post(login_url, {'username': user.email})
    assert not res.wsgi_request.user.is_authenticated

    mail_body = mailoutbox[0].body
    re_match = re.search(r'^https://[\w.-]*(.*)$', mail_body, re.MULTILINE)
    url = re_match.group(1)
    res = client.get(url, follow=True)
    assert res.status_code == 200
    assert 'Vous êtes maintenant connecté·e' in res.content.decode()
    assert res.wsgi_request.user.is_authenticated


def test_login_with_wrong_token(client, user, mailoutbox):
    login_url = reverse('password_reset')
    res = client.post(login_url, {'username': user.email})
    assert not res.wsgi_request.user.is_authenticated

    mail_body = mailoutbox[0].body
    re_match = re.search(
        r'^https://[\w.-]*/comptes/connexion/(.*)/(.*)/$',
        mail_body,
        re.MULTILINE)
    uidb64 = re_match.group(1)
    url = reverse('token_login', args=[uidb64, 'wrong_token'])
    res = client.get(url, follow=True)
    assert res.status_code == 200
    assert 'Quelque chose s\'est mal passé' in res.content.decode()
    assert not res.wsgi_request.user.is_authenticated


def test_login_with_wrong_user_id(client, user, mailoutbox):
    login_url = reverse('password_reset')
    res = client.post(login_url, {'username': user.email})
    assert not res.wsgi_request.user.is_authenticated

    mail_body = mailoutbox[0].body
    re_match = re.search(
        r'^https://[\w.-]*/comptes/connexion/(.*)/(.*)/$',
        mail_body,
        re.MULTILINE)
    token = re_match.group(2)
    url = reverse('token_login', args=['wrong_uid', token])
    res = client.get(url, follow=True)
    assert res.status_code == 200
    assert 'Quelque chose s\'est mal passé' in res.content.decode()
    assert not res.wsgi_request.user.is_authenticated


def test_register_form_is_for_anonymous_only(client, user):
    client.force_login(user)
    register_url = reverse('register')
    res = client.get(register_url)
    assert res.status_code == 302


def test_register_form_is_accessible_to_anonymous_user(client):
    register_url = reverse('register')
    res = client.get(register_url)
    assert res.status_code == 200


def test_register_form_expects_valid_data(client):
    register_url = reverse('register')
    res = client.post(
        register_url,
        {'first_name': '', 'last_name': '', 'email': 'tar@tiflet.te'})
    assert res.status_code == 200
    assert 'Ce champ est obligatoire' in res.content.decode()

    res = client.post(
        register_url,
        {'first_name': 'Petit', 'last_name': 'Pifou', 'email': 'tartiflette'})
    assert res.status_code == 200
    assert ' vérifier votre saisie ' in res.content.decode()


def test_register_form_with_unique_email(client, user, mailoutbox):
    """When registering with an existing email, just send a new login form."""

    register_url = reverse('register')
    res = client.post(
        register_url,
        {'first_name': 'New', 'last_name': 'User', 'email': user.email})
    assert res.status_code == 302
    assert len(mailoutbox) == 1

    mail = mailoutbox[0]
    assert mail.subject == 'Connexion à Aides-territoires'


def test_register_form(client, mailoutbox):
    users = User.objects.all()
    assert users.count() == 0

    register_url = reverse('register')
    res = client.post(
        register_url,
        {'first_name': 'Olga', 'last_name': 'Tau', 'email': 'olga@test.com'})

    assert res.status_code == 302
    assert len(mailoutbox) == 1
    assert users.count() == 1

    user = users[0]
    assert user.email == 'olga@test.com'
    assert user.first_name == 'Olga'
    assert user.last_name == 'Tau'
    assert not user.ml_consent

    mail = mailoutbox[0]
    assert mail.subject == 'Connexion à Aides-territoires'


def test_register_form_with_consent(client):
    users = User.objects.all()
    assert users.count() == 0

    register_url = reverse('register')
    res = client.post(register_url, {
        'first_name': 'Olga',
        'last_name': 'Tau',
        'email': 'olga@test.com',
        'ml_consent': True})

    assert res.status_code == 302
    assert users.count() == 1

    user = users[0]
    assert user.ml_consent


def test_register_form_converts_email_to_lowercase(client):
    users = User.objects.all()
    assert users.count() == 0

    register_url = reverse('register')
    res = client.post(register_url, {
        'first_name': 'Olga',
        'last_name': 'Tau',
        'email': 'OLGA@Test.Com',
        'ml_consent': True})

    assert res.status_code == 302
    assert users.count() == 1

    user = users[0]
    assert user.email == 'olga@test.com'


def test_profile_form_updates_profile(client, contributor):
    """The profile forms updates the contributor's data."""
    contributor.first_name = 'Donald'
    contributor.organization = 'La bande à Picsou'
    contributor.save()

    client.force_login(contributor)
    profile_url = reverse('contributor_profile')
    data = {
        'first_name': 'Anna',
        'last_name': 'NanananaBatman',
        'organization': 'Les Rapetou',
        'role': contributor.role,
        'contact_phone': contributor.contact_phone,
    }
    client.post(profile_url, data)

    contributor.refresh_from_db()
    assert contributor.full_name == 'Anna NanananaBatman'
    assert contributor.organization == 'Les Rapetou'


def test_profile_form_can_update_password(client, contributor):
    """The profile form can update the contributor's password."""

    new_password = 'New unpredictable passw0rd!'

    client.force_login(contributor)
    profile_url = reverse('contributor_profile')
    data = {
        'first_name': contributor.first_name,
        'last_name': contributor.last_name,
        'organization': contributor.organization,
        'role': contributor.role,
        'contact_phone': contributor.contact_phone,
        'new_password': new_password,
    }
    client.post(profile_url, data)

    assert authenticate(
        username=contributor.email, password=new_password) is not None


def test_profile_form_leaves_password_untouched(client, contributor):
    """By default, the profile form does not update the password."""

    client.force_login(contributor)
    profile_url = reverse('contributor_profile')
    data = {
        'first_name': contributor.first_name,
        'last_name': contributor.last_name,
        'organization': contributor.organization,
        'role': contributor.role,
        'contact_phone': contributor.contact_phone,
        'new_password': '',
    }
    client.post(profile_url, data)

    # "pass" is UserFactory's default password
    assert authenticate(
        username=contributor.email, password='pass') is not None
