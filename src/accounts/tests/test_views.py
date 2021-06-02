"""Test user login views."""

import pytest
import re

from django.contrib.auth import authenticate
from django.test import override_settings
from django.urls import reverse

from accounts.models import User
from accounts.factories import UserFactory
from search.factories import SearchPageFactory


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
    assert 'Vous êtes maintenant connecté' in res.content.decode()
    assert res.wsgi_request.user.is_authenticated


@override_settings(SIB_WELCOME_EMAIL_ENABLED=True)
def test_welcome_email_sent_on_token_login_success(client, user, mailoutbox):
    test_login_email_token_works(client, user, mailoutbox)
    # The first email is the token activation link, the second
    # is expected to be the welcome email.
    assert len(mailoutbox) == 2


@override_settings(SIB_WELCOME_EMAIL_ENABLED=False)
def test_welcome_email_not_sent_if_disabled(client, user, mailoutbox):
    test_login_email_token_works(client, user, mailoutbox)
    # The first email is the token activation link, the second
    # email should not be sent.
    assert len(mailoutbox) == 1


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
    res = client.post(register_url, {
        'first_name': '',
        'last_name': '',
        'email': 'tar@tiflet.te',
        'password1': 'Gloubiboulga',
        'password2': 'Gloubiboulga',
        'organization': '',
        'role': '',
        'contact_phone': '',
    })
    assert res.status_code == 200
    assert 'Ce champ est obligatoire' in res.content.decode()

    res = client.post(register_url, {
        'first_name': 'Petit',
        'last_name': 'Pifou',
        'password1': 'Gloubiboulga',
        'password2': 'Gloubiboulga',
        'email': 'tartiflette',
        'organization': 'Pif Magazine',
        'role': 'Héro',
        'contact_phone': '012345678',

    })
    assert res.status_code == 200
    assert ' vérifier votre saisie ' in res.content.decode()


def test_register_form_with_unique_email(client, user, mailoutbox):
    """When registering with an existing email, just send a new login form."""

    register_url = reverse('register')
    res = client.post(
        register_url, {
            'first_name': 'New',
            'last_name': 'User',
            'email': user.email,
            'password1': 'Gloubiboulga',
            'password2': 'Gloubiboulga',
            'organization': 'Test',
            'role': 'Tester',
            'contact_phone': '0123456779',
        })
    assert res.status_code == 302
    assert len(mailoutbox) == 1

    mail = mailoutbox[0]
    assert mail.subject == 'Connexion à Aides-territoires'


def test_register_form(client, mailoutbox):
    users = User.objects.all()
    assert users.count() == 0

    register_url = reverse('register')
    res = client.post(register_url, {
        'first_name': 'Olga',
        'last_name': 'Tau',
        'email': 'olga@test.com',
        'password1': 'Gloubiboulga',
        'password2': 'Gloubiboulga',
        'organization': 'Test',
        'role': 'Tester',
        'contact_phone': '0123456779',
    })

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


def test_register_form_converts_email_to_lowercase(client):
    users = User.objects.all()
    assert users.count() == 0

    register_url = reverse('register')
    res = client.post(register_url, {
        'first_name': 'Olga',
        'last_name': 'Tau',
        'email': 'OLGA@Test.Com',
        'password1': 'Gloubiboulga',
        'password2': 'Gloubiboulga',
        'organization': 'Test',
        'role': 'Tester',
        'contact_phone': '0123456779'
    })
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


def test_logged_in_contributor_has_menu(client, contributor):
    client.force_login(contributor)
    home = reverse('home')
    res = client.get(home)
    assert 'Votre profil' in res.content.decode()
    assert 'Espace contributeur' in res.content.decode()


def test_logged_in_staff_has_menu(client):
    user_staff = UserFactory(is_superuser=True, is_contributor=False)
    client.force_login(user_staff)
    home = reverse('home')
    res = client.get(home)
    assert 'Votre profil' in res.content.decode()
    assert 'Espace contributeur' in res.content.decode()


def test_non_contributor_can_log_in_but_no_menu(client):
    user_api = UserFactory(is_contributor=False)
    client.force_login(user_api)
    home = reverse('home')
    res = client.get(home)
    assert 'Votre profil' not in res.content.decode()
    assert 'Espace contributeur' not in res.content.decode()


def test_search_page_administrator_has_specific_menu(client):
    user_admin_pp = UserFactory(is_contributor=False)
    pp = SearchPageFactory(title='Test PP')
    pp.administrators.add(user_admin_pp)
    client.force_login(user_admin_pp)
    home = reverse('home')
    res = client.get(home)
    assert 'Test PP' in res.content.decode()
