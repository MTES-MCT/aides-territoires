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
    user = UserFactory(
        email="invite.sender@example.org", beneficiary_organization=organization
    )
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
    user = UserFactory(
        beneficiary_organization=organization, email="invite.sender@example.org"
    )
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
    user = UserFactory(
        beneficiary_organization=organization, email="invite.sender@example.org"
    )
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


def test_an_invitation_email_is_sent_to_user_with_no_existing_account(
    client, mailoutbox
):
    """An email is send to the invited user with no existing account"""

    organization = OrganizationFactory()
    user = UserFactory(
        beneficiary_organization=organization, email="invite.sender@example.org"
    )
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


def test_an_invitation_email_is_sent_to_user_with_an_existing_account(
    client, mailoutbox
):
    """An email is send to the invited user with an existing account"""

    organization = OrganizationFactory()
    organization2 = OrganizationFactory()
    user = UserFactory(
        beneficiary_organization=organization, email="invite.sender@example.org"
    )
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

    current_organization = OrganizationFactory()
    organization2 = OrganizationFactory()
    invitation_author = UserFactory(
        email="author.oftheinvitation@example.org",
        beneficiary_organization=organization2,
    )
    user = UserFactory(
        beneficiary_organization=current_organization,
        proposed_organization=organization2,
        invitation_author=invitation_author,
        email="willrefuse.invite@example.org",
    )
    current_organization.beneficiaries.add(user)
    current_organization.save()

    client.force_login(user)

    join_organization_url = reverse("join_organization")
    res = client.post(
        join_organization_url,
        {
            "no-join": True,
        },
    )

    assert res.status_code == 302

    user.refresh_from_db()
    assert user.beneficiary_organization == current_organization
    assert user.proposed_organization is None

    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    assert (
        mail.subject == "Rejet de votre invitation à collaborer sur Aides-territoires"
    )

    user_dashboard_page = reverse("user_dashboard")
    res = client.get(user_dashboard_page, follow=True)
    assert "Votre refus a bien été pris en compte." in res.content.decode()


def test_invited_user_can_join_a_new_organization(client, mailoutbox):

    current_organization = OrganizationFactory()
    new_organization = OrganizationFactory()
    invitation_author = UserFactory(
        email="author.oftheinvitation@example.org",
        beneficiary_organization=new_organization,
    )
    user = UserFactory(
        beneficiary_organization=current_organization,
        proposed_organization=new_organization,
        invitation_author=invitation_author,
        email="willjoin.neworg@example.org",
    )
    current_organization.beneficiaries.add(user)
    current_organization.save()
    new_organization.beneficiaries.add(invitation_author)
    new_organization.save()

    client.force_login(user)

    join_organization_url = reverse("join_organization")
    res = client.post(
        join_organization_url,
        {
            "yes-join": True,
        },
    )

    assert res.status_code == 302

    user.refresh_from_db()
    assert user.beneficiary_organization == new_organization
    assert user.proposed_organization is None
    assert new_organization.beneficiaries.count() == 2

    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    assert (
        mail.subject
        == "Votre invitation à collaborer sur Aides-territoires a été acceptée"
    )

    user_dashboard_page = reverse("user_dashboard")
    res = client.get(user_dashboard_page, follow=True)
    assert "Félicitations, vous avez rejoint la structure" in res.content.decode()


def test_email_is_send_to_former_collaborators_to_notice_them_the_leaving(
    client, mailoutbox
):
    # If the invited user join the new organization
    # and was not the only member of the previous organization,
    # an email is send to the former collaborators of the user to notice them the departure

    current_organization = OrganizationFactory()
    new_organization = OrganizationFactory()
    invitation_author = UserFactory(
        email="author.oftheinvitation@example.org",
        beneficiary_organization=new_organization,
    )
    former_collaborator = UserFactory(
        email="former.collaborator@example.org",
        beneficiary_organization=current_organization,
    )
    user = UserFactory(
        beneficiary_organization=current_organization,
        proposed_organization=new_organization,
        invitation_author=invitation_author,
        email="invited.user@example.org",
    )
    current_organization.beneficiaries.add(former_collaborator)
    current_organization.beneficiaries.add(user)
    current_organization.save()

    client.force_login(user)

    join_organization_url = reverse("join_organization")
    res = client.post(
        join_organization_url,
        {
            "yes-join": True,
        },
    )

    assert res.status_code == 302

    user.refresh_from_db()
    assert user.beneficiary_organization == new_organization
    assert user.proposed_organization is None

    assert len(mailoutbox) == 2
    mail1 = mailoutbox[0]
    mail2 = mailoutbox[1]
    assert (
        mail1.subject
        == "Un collaborateur a quitté votre structure sur Aides-territoires"
    )
    assert (
        mail2.subject
        == "Votre invitation à collaborer sur Aides-territoires a été acceptée"
    )

    user_dashboard_page = reverse("user_dashboard")
    res = client.get(user_dashboard_page, follow=True)
    assert "Félicitations, vous avez rejoint la structure" in res.content.decode()


def test_email_can_be_send_to_former_collaborators_to_invite_them_to_join(
    client, mailoutbox
):
    # If the invited user join the new organization
    # and was not the only member of the previous organization,
    # he can invite former collaborators to join the new organization

    current_organization = OrganizationFactory()
    new_organization = OrganizationFactory()
    invitation_author = UserFactory(
        email="author.oftheinvitation@example.org",
        beneficiary_organization=new_organization,
    )
    former_collaborator = UserFactory(
        email="former.collaborator@example.org",
        beneficiary_organization=current_organization,
    )
    user = UserFactory(
        beneficiary_organization=current_organization,
        proposed_organization=new_organization,
        invitation_author=invitation_author,
        email="invited.user@example.org",
    )
    current_organization.beneficiaries.add(former_collaborator)
    current_organization.beneficiaries.add(user)
    current_organization.save()

    client.force_login(user)

    join_organization_url = reverse("join_organization")
    res = client.post(
        join_organization_url,
        {
            "collaborators": [
                former_collaborator.id,
            ],
            "yes-join": True,
        },
    )

    assert res.status_code == 302

    user.refresh_from_db()
    assert user.beneficiary_organization == new_organization
    assert user.proposed_organization is None

    assert len(mailoutbox) == 3
    mail = mailoutbox[0]
    assert mail.subject == "invitation à collaborer sur Aides-territoires"

    user_dashboard_page = reverse("user_dashboard")
    res = client.get(user_dashboard_page, follow=True)
    assert "Félicitations, vous avez rejoint la structure" in res.content.decode()
