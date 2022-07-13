"""Test invite collaborator and fusion organization functionnalities."""

import pytest

from django.urls import reverse

from accounts.factories import UserFactory
from organizations.factories import OrganizationFactory

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_access_invite_collaborator_form(client):
    invite_collaborator_url = reverse("invite_collaborator")
    res = client.get(invite_collaborator_url)
    assert res.status_code == 302


def test_invite_collaborator_form_expects_valid_data(client, user):
    client.force_login(user)
    invite_collaborator_url = reverse("invite_collaborator")
    res = client.post(
        invite_collaborator_url,
        {
            "first_name": "tar",
            "last_name": "tiflet",
            "email": "",
        },
    )
    assert res.status_code == 200
    assert "Ce champ est obligatoire" in res.content.decode()


def test_cant_invite_a_current_collaborator(client):
    """When inviting a user with a current collaborator email, there is a warning"""

    organization = OrganizationFactory()
    user = UserFactory(beneficiary_organization=organization)
    user2 = UserFactory(
        email="isalready.ourcollaborator@example.org",
        beneficiary_organization=organization,
    )
    organization.beneficiaries.add(user)
    organization.beneficiaries.add(user2)
    organization.save()

    client.force_login(user)
    invite_collaborator_url = reverse("invite_collaborator")
    res = client.post(
        invite_collaborator_url,
        {
            "first_name": "New",
            "last_name": "Collaborator",
            "email": "isalready.ourcollaborator@example.org",
        },
    )
    assert res.status_code == 200
    assert "Cet utilisateur est déjà un de vos collaborateurs." in res.content.decode()


def test_cant_invite_user_with_an_existing_invitation(client, user):
    """When inviting a user that already has an invitation, there is a warning"""

    organization = OrganizationFactory()
    UserFactory(
        email="hassalready.aninvitation@example.org", proposed_organization=organization
    )

    client.force_login(user)
    invite_collaborator_url = reverse("invite_collaborator")
    res = client.post(
        invite_collaborator_url,
        {
            "first_name": "New",
            "last_name": "Collaborator",
            "email": "hassalready.aninvitation@example.org",
        },
    )
    assert res.status_code == 200
    assert (
        "Cet utilisateur ne peut être invité car il a déjà une invitation en attente."
        in res.content.decode()
    )


def test_can_invite_user_with_an_existing_account(client):
    """It is possible to invite a user that already has an account"""

    organization = OrganizationFactory()
    organization2 = OrganizationFactory()
    user = UserFactory(beneficiary_organization=organization)
    user2 = UserFactory(
        email="hasalready.anaccount@example.org", beneficiary_organization=organization2
    )
    organization.beneficiaries.add(user)
    organization.save()
    organization2.beneficiaries.add(user2)
    organization2.save()

    client.force_login(user)

    invite_collaborator_url = reverse("invite_collaborator")
    res = client.post(
        invite_collaborator_url,
        {
            "first_name": "New",
            "last_name": "Collaborator",
            "email": "hasalready.anaccount@example.org",
        },
    )
    assert res.status_code == 302
    user2.refresh_from_db()
    assert user2.proposed_organization == organization
    assert user2.invitation_author == user
    collaborator_list_page = reverse("collaborators")
    res = client.get(collaborator_list_page, follow=True)
    assert (
        "Votre invitation a bien été envoyée ; l'utilisateur invité pourra accepter ou non votre invitation."  # noqa
        in res.content.decode()
    )


def test_can_invite_user_with_no_existing_account(client):
    """It is possible to invite a user that already has an account"""

    organization = OrganizationFactory()
    user = UserFactory(beneficiary_organization=organization)
    organization.beneficiaries.add(user)
    organization.save()

    client.force_login(user)

    invite_collaborator_url = reverse("invite_collaborator")
    res = client.post(
        invite_collaborator_url,
        {
            "first_name": "New",
            "last_name": "Collaborator",
            "email": "hasno.account@example.org",
        },
    )
    assert res.status_code == 302
    collaborator_list_page = reverse("collaborators")
    res = client.get(collaborator_list_page, follow=True)
    assert "Votre invitation a bien été envoyée" in res.content.decode()


def test_an_invitation_email_is_sent_to_user_with_no_existing_account(client, mailoutbox):
    """An email is send to the invited user with no existing account"""

    organization = OrganizationFactory()
    user = UserFactory(beneficiary_organization=organization)
    organization.beneficiaries.add(user)
    organization.save()

    client.force_login(user)

    invite_collaborator_url = reverse("invite_collaborator")
    res = client.post(
        invite_collaborator_url,
        {
            "first_name": "New",
            "last_name": "Collaborator",
            "email": "hasno.account@example.org",
        },
    )

    assert res.status_code == 302
    assert len(mailoutbox) == 1

    mail = mailoutbox[0]
    assert mail.subject == "invitation à collaborer sur Aides-territoires"


def test_an_invitation_email_is_sent_to_user_with_an_existing_account(client, mailoutbox):
    """An email is send to the invited user with an existing account"""

    organization = OrganizationFactory()
    organization2 = OrganizationFactory()
    user = UserFactory(beneficiary_organization=organization)
    user2 = UserFactory(
        email="hasalready.anaccount@example.org", beneficiary_organization=organization2
    )
    organization.beneficiaries.add(user)
    organization.save()
    organization2.beneficiaries.add(user2)
    organization2.save()

    client.force_login(user)

    invite_collaborator_url = reverse("invite_collaborator")
    res = client.post(
        invite_collaborator_url,
        {
            "first_name": "New",
            "last_name": "Collaborator",
            "email": "hasalready.anaccount@example.org",
        },
    )

    assert res.status_code == 302
    assert len(mailoutbox) == 1

    mail = mailoutbox[0]
    assert mail.subject == "invitation à collaborer sur Aides-territoires"


def test_invited_user_can_refuse_to_join_a_new_organization(client, mailoutbox):
    """An email is send to the invited user with an existing account"""
    
    organization = OrganizationFactory()
    organization2 = OrganizationFactory()
    invitation_author = UserFactory(email="author.oftheinvitation@example.org", beneficiary_organization=organization2)
    user = UserFactory(beneficiary_organization=organization, proposed_organization=organization2, invitation_author=invitation_author)
    organization.beneficiaries.add(user)
    organization.save()

    client.force_login(user)

    join_organization_url = reverse('join_organization')
    res = client.post(
        join_organization_url,
        {
            "no-join": True,
        },
    )

    assert res.status_code == 302

    user.refresh_from_db()
    assert user.beneficiary_organization == organization
    assert user.proposed_organization == None

    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    assert mail.subject == "Rejet de votre invitation à collaborer sur Aides-territoires"
    
    user_dashboard_page = reverse("user_dashboard")
    res = client.get(user_dashboard_page, follow=True)
    assert "Votre refus a bien été pris en compte." in res.content.decode()
