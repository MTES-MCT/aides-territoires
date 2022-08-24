"""Test user login views."""

import pytest
import re

from django.conf import settings
from django.contrib.auth import authenticate
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from accounts.factories import UserFactory
from aids.factories import AidFactory
from alerts.factories import AlertFactory
from alerts.models import Alert
from organizations.models import Organization
from projects.factories import ProjectFactory
from search.factories import SearchPageFactory
from django.contrib.auth.hashers import check_password
from geofr.models import Perimeter

pytestmark = pytest.mark.django_db


def test_login_view_is_for_anonymous_only(client, user):
    """Authenticated users cannot login again, duh!"""

    client.force_login(user)
    login_url = reverse("login")
    res = client.get(login_url)
    assert res.status_code == 302


def test_login_view_is_accessible_for_anonymous_users(client):
    login_url = reverse("login")
    res = client.get(login_url)
    assert res.status_code == 200


def test_login_is_case_insensitive(client, user):
    user.email = "test@test.com"
    user.set_password("DefaultPassword!")
    user.save()

    login_url = reverse("login")
    res = client.get(login_url)
    assert res.status_code == 200
    assert not res.wsgi_request.user.is_authenticated

    res = client.post(
        login_url, {"username": "TEST@TEST.com", "password": "DefaultPassword!"}
    )
    assert res.status_code == 302
    assert res.wsgi_request.user.is_authenticated


def test_password_reset_with_existing_email_does_send_an_email(
    client, user, mailoutbox
):
    login_url = reverse("password_reset")
    res = client.post(login_url, {"username": user.email})
    assert res.status_code == 302
    assert len(mailoutbox) == 1

    mail = mailoutbox[0]
    assert mail.subject == "Renouvellement de votre mot de passe"


def test_login_email_token_works(client, user, mailoutbox):
    login_url = reverse("password_reset")
    res = client.post(login_url, {"username": user.email})
    assert not res.wsgi_request.user.is_authenticated

    mail_body = mailoutbox[0].body
    re_match = re.search(
        r"^https://[\w.-]*/comptes/connexion/(.*)/(.*)/(.*)$", mail_body, re.MULTILINE
    )
    url = re_match.group(0)
    res = client.get(url, follow=True)
    assert res.status_code == 200
    assert "Vous êtes maintenant connecté" in res.content.decode()
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
    login_url = reverse("password_reset")
    res = client.post(login_url, {"username": user.email})
    assert not res.wsgi_request.user.is_authenticated

    mail_body = mailoutbox[0].body
    re_match = re.search(
        r"^https://[\w.-]*/comptes/connexion/(.*)/(.*)/(.*)$", mail_body, re.MULTILINE
    )
    uidb64 = re_match.group(2)
    url = reverse("token_login", args=[uidb64, "wrong_token"])
    res = client.get(url, follow=True)
    assert res.status_code == 200
    assert "Quelque chose s’est mal passé" in res.content.decode()
    assert not res.wsgi_request.user.is_authenticated


def test_login_with_wrong_user_id(client, user, mailoutbox):
    login_url = reverse("password_reset")
    res = client.post(login_url, {"username": user.email})
    assert not res.wsgi_request.user.is_authenticated

    mail_body = mailoutbox[0].body
    re_match = re.search(
        r"^https://[\w.-]*/comptes/connexion/(.*)/(.*)/(.*)$", mail_body, re.MULTILINE
    )
    token = re_match.group(2)
    url = reverse("token_login", args=["wrong_uid", token])
    res = client.get(url, follow=True)
    assert res.status_code == 200
    assert "Quelque chose s’est mal passé" in res.content.decode()
    assert not res.wsgi_request.user.is_authenticated


def test_register_form_is_for_anonymous_only(client, user):
    client.force_login(user)
    register_url = reverse("register")
    res = client.get(register_url)
    assert res.status_code == 302


def test_register_form_is_accessible_to_anonymous_user(client):
    register_url = reverse("register")
    res = client.get(register_url)
    assert res.status_code == 200


def test_register_form_expects_valid_data(client, perimeters):
    register_url = reverse("register")
    res = client.post(
        register_url,
        {
            "first_name": "",
            "last_name": "",
            "email": "tar@tiflet.te",
            "password1": "Gloubiboulga",
            "password2": "Gloubiboulga",
            "organization_type": "farmer",
            "perimeter": perimeters["france"].id,
            "organization_name": "L'île aux enfants",
            "beneficiary_role": "Pas de la tarte",
            "beneficiary_function": "other",
            "is_beneficiary": True,
            "is_contributor": False,
        },
    )
    assert res.status_code == 200
    assert "Ce champ est obligatoire" in res.content.decode()

    res = client.post(
        register_url,
        {
            "first_name": "Petit",
            "last_name": "Pifou",
            "password1": "Gloubiboulga",
            "password2": "Gloubiboulga",
            "email": "tartiflette",
            "organization_type": "farmer",
            "perimeter": perimeters["france"].id,
            "organization_name": "L'île aux enfants",
            "beneficiary_role": "Pas de la tarte",
            "beneficiary_function": "other",
            "is_beneficiary": True,
            "is_contributor": False,
        },
    )
    assert res.status_code == 200
    assert "Saisissez une adresse e-mail valide." in res.content.decode()


def test_register_form_with_unique_email(client, user, mailoutbox, perimeters):
    """When registering with an existing email, there is a warning"""

    register_url = reverse("register")
    res = client.post(
        register_url,
        {
            "first_name": "New",
            "last_name": "User",
            "email": user.email,
            "password1": "Gloubiboulga",
            "password2": "Gloubiboulga",
            "organization_type": "farmer",
            "perimeter": perimeters["france"].id,
            "organization_name": "L'île aux enfants",
            "beneficiary_role": "Pas de la tarte",
            "beneficiary_function": "other",
            "is_beneficiary": True,
            "is_contributor": False,
        },
    )
    assert res.status_code == 200
    assert (
        "Un objet Utilisateur avec ce champ Adresse e-mail existe déjà"
        in res.content.decode()
    )


def test_register_form(client, mailoutbox, perimeters):
    users = User.objects.all()
    organizations = Organization.objects.all()
    assert users.count() == 0
    assert organizations.count() == 0

    register_url = reverse("register")
    res = client.post(
        register_url,
        {
            "first_name": "Olga",
            "last_name": "Tau",
            "email": "olga@test.com",
            "password1": "Gloubiboulga",
            "password2": "Gloubiboulga",
            "perimeter": perimeters["france"].id,
            "organization_name": "L'île aux enfants",
            "organization_type": "farmer",
            "beneficiary_role": "Pas de la tarte",
            "beneficiary_function": "other",
            "is_beneficiary": True,
            "is_contributor": False,
        },
    )

    assert res.status_code == 302

    assert len(mailoutbox) == 1
    assert users.count() == 1
    assert organizations.count() == 1

    user = users[0]
    assert user.email == "olga@test.com"
    assert user.first_name == "Olga"
    assert user.last_name == "Tau"
    assert not user.ml_consent
    organization = organizations[0]
    assert organization.name == "L'île aux enfants"

    mail = mailoutbox[0]
    assert mail.subject == "Connexion à Aides-territoires"


def test_register_form_converts_email_to_lowercase(client, perimeters):
    users = User.objects.all()
    assert users.count() == 0

    register_url = reverse("register")
    res = client.post(
        register_url,
        {
            "first_name": "Olga",
            "last_name": "Tau",
            "email": "OLGA@Test.Com",
            "password1": "Gloubiboulga",
            "password2": "Gloubiboulga",
            "perimeter": perimeters["france"].id,
            "organization_name": "L'île aux enfants",
            "organization_type": "farmer",
            "beneficiary_role": "Pas de la tarte",
            "beneficiary_function": "other",
            "is_beneficiary": True,
            "is_contributor": False,
        },
    )
    assert res.status_code == 302
    assert users.count() == 1

    user = users[0]
    assert user.email == "olga@test.com"


def test_profile_form_updates_profile(client, contributor):
    """The profile forms updates the contributor's data."""
    contributor.first_name = "Donald"
    contributor.beneficiary_role = "Canard vivant"
    contributor.save()

    client.force_login(contributor)
    profile_url = reverse("contributor_profile")
    data = {
        "first_name": "Anna",
        "last_name": "NanananaBatman",
        "email": contributor.email,
        "is_contributor": contributor.is_contributor,
        "is_beneficiary": contributor.is_beneficiary,
        "beneficiary_function": contributor.beneficiary_function,
        "beneficiary_role": "Chauve-souris milliardaire",
        "new_password": "",
        "new_password2": "",
        "current_password": "",
    }
    client.post(profile_url, data, follow=True)

    contributor.refresh_from_db()
    assert contributor.full_name == "Anna NanananaBatman"
    assert contributor.beneficiary_role == "Chauve-souris milliardaire"


def test_profile_form_leaves_password_untouched(client, contributor):
    """By default, the profile form does not update the password."""

    client.force_login(contributor)
    profile_url = reverse("contributor_profile")
    data = {
        "first_name": "Update name",
        "last_name": contributor.last_name,
        "email": contributor.email,
        "is_contributor": contributor.is_contributor,
        "is_beneficiary": contributor.is_beneficiary,
        "beneficiary_function": contributor.beneficiary_function,
        "beneficiary_role": contributor.beneficiary_role,
        "new_password": "",
        "new_password2": "",
    }
    client.post(profile_url, data, follow=True)

    contributor.refresh_from_db()

    # "DefaultPassword!" is UserFactory's default password
    assert (
        authenticate(username=contributor.email, password="DefaultPassword!")
        is not None
    )


def test_profile_form_cant_update_password_without_entering_the_current_one(
    client, contributor
):
    """The profile form can't update the contributor's password if the current one isn't entered."""

    registered_password = contributor.password
    new_password = "New unpredictable passw0rd!"

    client.force_login(contributor)
    profile_url = reverse("contributor_profile")
    data = {
        "first_name": contributor.first_name,
        "last_name": contributor.last_name,
        "email": contributor.email,
        "is_contributor": contributor.is_contributor,
        "is_beneficiary": contributor.is_beneficiary,
        "beneficiary_function": contributor.beneficiary_function,
        "beneficiary_role": contributor.beneficiary_role,
        "new_password": new_password,
        "new_password2": new_password,
        "current_password": "",
    }

    res = client.post(profile_url, data, follow=True)
    contributor.refresh_from_db()
    assert contributor.password == registered_password
    assert (
        "Vous devez entrer votre mot de passe actuel pour pouvoir le changer."
        in res.content.decode()
    )


def test_profile_form_cant_update_password_while_entering_a_wrong_current_one(
    client, contributor
):
    """The profile form can't update the contributor's password."""

    registered_password = contributor.password
    new_password = "New unpredictable passw0rd!"

    client.force_login(contributor)
    profile_url = reverse("contributor_profile")
    data = {
        "first_name": contributor.first_name,
        "last_name": contributor.last_name,
        "email": contributor.email,
        "is_contributor": contributor.is_contributor,
        "is_beneficiary": contributor.is_beneficiary,
        "beneficiary_function": contributor.beneficiary_function,
        "beneficiary_role": contributor.beneficiary_role,
        "new_password": new_password,
        "new_password2": new_password,
        "current_password": "WrongPassword!",
    }

    res = client.post(profile_url, data, follow=True)
    contributor.refresh_from_db()
    assert contributor.password == registered_password
    assert "Le mot de passe actuel entré est incorrect." in res.content.decode()


def test_profile_form_cant_update_non_matching_passwords(client, contributor):
    """
    The profile form can update the contributor's password if the two
    values in the new password are distinct
    """

    new_password = "New unpredictable passw0rd!"

    client.force_login(contributor)
    profile_url = reverse("contributor_profile")
    data = {
        "first_name": contributor.first_name,
        "last_name": "Nouveau",
        "email": contributor.email,
        "is_contributor": contributor.is_contributor,
        "is_beneficiary": contributor.is_beneficiary,
        "beneficiary_function": contributor.beneficiary_function,
        "beneficiary_role": contributor.beneficiary_role,
        "new_password": new_password,
        "new_password2": "Oops I did it again",
        "current_password": "DefaultPassword!",
    }

    res = client.post(profile_url, data, follow=True)
    contributor.refresh_from_db()

    assert check_password("DefaultPassword!", contributor.password)
    assert "Les mots de passe ne sont pas identiques" in res.content.decode()


def test_profile_form_can_update_password(client, contributor):
    """The profile form can update the contributor's password."""

    new_password = "New unpredictable passw0rd!"

    client.force_login(contributor)
    profile_url = reverse("contributor_profile")
    data = {
        "first_name": contributor.first_name,
        "last_name": "Nouveau",
        "email": contributor.email,
        "is_contributor": contributor.is_contributor,
        "is_beneficiary": contributor.is_beneficiary,
        "beneficiary_function": contributor.beneficiary_function,
        "beneficiary_role": contributor.beneficiary_role,
        "new_password": new_password,
        "new_password2": new_password,
        "current_password": "DefaultPassword!",
    }

    client.post(profile_url, data, follow=True)
    contributor.refresh_from_db()

    assert check_password(new_password, contributor.password)
    assert authenticate(username=contributor.email, password=new_password) is not None


def test_search_page_administrator_has_specific_menu(client):
    user_admin_pp = UserFactory(is_contributor=False, email="admin.pp@example.org")
    user_org = Organization(name="Sample Org", perimeter=Perimeter.objects.first())
    user_org.save()
    user_admin_pp.beneficiary_organization_id = user_org.pk
    user_admin_pp.organization_type = "farmer"
    user_admin_pp.save()

    SearchPageFactory(title="Test Page portail", administrator=user_admin_pp)
    client.force_login(user_admin_pp)
    profile_page = reverse("contributor_profile")
    res = client.get(profile_page, follow=True)

    assert "Test Page portail" in res.content.decode()


def test_user_deletion_form_deletes_the_account(client, contributor):
    client.force_login(contributor)
    user_deletion_url = reverse("delete_user_account")
    data = {}
    client.post(user_deletion_url, data, follow=True)

    assert User.objects.filter(email=contributor.email).count() == 0


def test_user_deletion_form_allows_to_delete_specific_alerts(client, contributor):
    client.force_login(contributor)

    AlertFactory(querystring="text=Garder", email=contributor.email)  # alert_to_keep
    alert_to_delete = AlertFactory(querystring="text=Effacer", email=contributor.email)

    user_deletion_url = reverse("delete_user_account")
    data = {f"alert-{alert_to_delete.pk}": True}
    client.post(user_deletion_url, data, follow=True)

    assert Alert.objects.count() == 1


def test_user_deletion_form_allows_to_reattribute_invitations(client, contributor):
    client.force_login(contributor)

    contributor_org = contributor.beneficiary_organization

    invited_user = UserFactory(
        email="invited@example.org",
        proposed_organization=contributor.beneficiary_organization,
        invitation_author=contributor,
        invitation_date=timezone.now(),
    )

    other_member = UserFactory(email="to.keep@example.org")
    other_member.beneficiary_organization = contributor_org
    other_member.save()

    contributor_org.beneficiaries.add(other_member)
    contributor_org.save()

    user_deletion_url = reverse("delete_user_account")
    data = {
        "invitations-transfer": other_member.id,
    }

    client.post(user_deletion_url, data, follow=True)
    invited_user.refresh_from_db()

    assert invited_user.invitation_author == other_member


def test_user_deletion_form_can_only_reattribute_invitations_to_org_members(
    client, contributor
):
    client.force_login(contributor)

    invited_user = UserFactory(
        email="invited@example.org",
        proposed_organization=contributor.beneficiary_organization,
        invitation_author=contributor,
        invitation_date=timezone.now(),
    )

    other_member = UserFactory(email="to.keep@example.org")

    user_deletion_url = reverse("delete_user_account")
    data = {
        "invitations-transfer": other_member.id,
    }

    res = client.post(user_deletion_url, data)
    invited_user.refresh_from_db()

    assert res.status_code == 404


def test_user_deletion_form_allows_to_reattribute_projects(client, contributor):
    client.force_login(contributor)

    contributor_org = contributor.beneficiary_organization

    other_member = UserFactory(is_contributor=False, email="to.keep@example.org")
    other_member.beneficiary_organization = contributor_org
    other_member.save()

    project_to_transfer = ProjectFactory(name="Projet à transférer")
    project_to_transfer.author.add(contributor)
    project_to_transfer.save()

    contributor_org.beneficiaries.add(other_member)
    contributor_org.project_set.add(project_to_transfer)
    contributor_org.save()

    user_deletion_url = reverse("delete_user_account")
    data = {
        "projects-transfer": other_member.id,
    }

    client.post(user_deletion_url, data, follow=True)
    project_to_transfer.refresh_from_db()

    assert project_to_transfer.author.first() == other_member


def test_user_deletion_form_can_only_reattribute_projects_to_org_members(
    client, contributor
):
    client.force_login(contributor)

    contributor_org = contributor.beneficiary_organization

    other_member = UserFactory(is_contributor=False, email="to.keep@example.org")
    other_member.save()

    project_to_transfer = ProjectFactory(name="Projet à transférer")
    project_to_transfer.author.add(contributor)
    project_to_transfer.save()

    contributor_org.project_set.add(project_to_transfer)
    contributor_org.save()

    user_deletion_url = reverse("delete_user_account")
    data = {
        "projects-transfer": other_member.id,
    }

    res = client.post(user_deletion_url, data, follow=True)
    project_to_transfer.refresh_from_db()

    assert res.status_code == 404


def test_user_deletion_form_allows_to_reattribute_aids(client, contributor):
    client.force_login(contributor)

    contributor_org = contributor.beneficiary_organization

    other_member = UserFactory(is_contributor=False, email="to.keep@example.org")
    other_member.beneficiary_organization = contributor_org
    other_member.save()

    contributor_org.beneficiaries.add(other_member)
    contributor_org.save()

    aid_to_transfer = AidFactory(author=contributor)

    user_deletion_url = reverse("delete_user_account")
    data = {
        "aids-transfer": other_member.id,
    }

    client.post(user_deletion_url, data, follow=True)
    aid_to_transfer.refresh_from_db()

    assert aid_to_transfer.author == other_member


def test_user_deletion_form_reattributes_aids_to_AT_admin_by_default(
    client, contributor
):
    """
    If the user does not choose to reattribute their aids to another member of their org,
    their aids are instead reattributed to AT admin (even if the org has other members)
    """
    client.force_login(contributor)

    contributor_org = contributor.beneficiary_organization

    other_member = UserFactory(is_contributor=False, email="to.keep@example.org")
    other_member.beneficiary_organization = contributor_org
    other_member.save()

    contributor_org.beneficiaries.add(other_member)
    contributor_org.save()

    aid_to_transfer = AidFactory(author=contributor)

    user_deletion_url = reverse("delete_user_account")
    data = {}

    client.post(user_deletion_url, data, follow=True)
    aid_to_transfer.refresh_from_db()

    at_admin = User.objects.get(email=settings.AT_ADMIN_EMAIL)

    assert aid_to_transfer.author == at_admin


def test_user_deletion_form_can_only_reattribute_aids_to_org_members(
    client, contributor
):
    client.force_login(contributor)

    other_member = UserFactory(is_contributor=False, email="to.keep@example.org")
    other_member.save()

    aid_to_transfer = AidFactory(author=contributor)

    user_deletion_url = reverse("delete_user_account")
    data = {
        "aids-transfer": other_member.id,
    }

    res = client.post(user_deletion_url, data, follow=True)
    aid_to_transfer.refresh_from_db()

    assert res.status_code == 404
