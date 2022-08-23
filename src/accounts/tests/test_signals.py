import pytest

from django.utils import timezone

from accounts.models import User
from accounts.signals import manage_user_content_before_deletion
from accounts.factories import UserFactory
from geofr.models import Perimeter
from organizations.models import Organization
from projects.factories import ProjectFactory
from projects.models import Project

pytestmark = pytest.mark.django_db

# mucbd: manage_user_content_before_deletion()


def test_mucbd_reattributes_projects_if_another_user_exists(client):
    user_org = Organization(name="Sample Org", perimeter=Perimeter.objects.first())
    user_org.save()

    user_to_delete = UserFactory(is_contributor=False, email="to.delete@example.org")
    user_to_delete.beneficiary_organization_id = user_org.pk
    user_to_delete.save()

    other_user = UserFactory(is_contributor=False, email="to.keep@example.org")
    other_user.beneficiary_organization_id = user_org.pk
    other_user.save()

    project_to_reattribute = ProjectFactory(name="Projet à réattribuer")
    project_to_reattribute.author.add(user_to_delete)
    project_to_reattribute.save()

    user_org.beneficiaries.add(user_to_delete, other_user)
    user_org.project_set.add(project_to_reattribute)
    user_org.save()

    manage_user_content_before_deletion(User, user_to_delete)

    assert project_to_reattribute.author.first().email == other_user.email


def test_mucbd_deletes_projects_if_no_user_exists(client):
    user_org = Organization(name="Sample Org", perimeter=Perimeter.objects.first())
    user_org.save()

    user_to_delete = UserFactory(is_contributor=False, email="to.delete@example.org")
    user_to_delete.beneficiary_organization_id = user_org.pk
    user_to_delete.save()

    project_to_delete = ProjectFactory(name="Projet à supprimer")
    project_to_delete.author.add(user_to_delete)
    project_to_delete.save()

    user_org.beneficiaries.add(user_to_delete)
    user_org.project_set.add(project_to_delete)
    user_org.save()

    manage_user_content_before_deletion(User, user_to_delete)
    projects = Project.objects.all()
    assert projects.count() == 0


def test_mucbd_deletes_invitations_to_existing_users(client):
    user_org = Organization(name="Sample Org", perimeter=Perimeter.objects.first())
    user_org.save()

    user_to_delete = UserFactory(is_contributor=False, email="to.delete@example.org")
    user_to_delete.beneficiary_organization_id = user_org.pk
    user_to_delete.save()

    invited_user = UserFactory(
        is_contributor=False,
        email="invited@example.org",
        proposed_organization=user_org,
        invitation_author=user_to_delete,
        invitation_date=timezone.now(),
    )

    user_org.beneficiaries.add(user_to_delete)
    user_org.save()

    manage_user_content_before_deletion(User, user_to_delete)

    assert User.objects.filter(invitation_author=user_to_delete).count() == 0


def test_mucbd_deletes_org_if_no_other_member(client):
    user_org = Organization(name="Org to delete", perimeter=Perimeter.objects.first())
    user_org.save()

    user_to_delete = UserFactory(is_contributor=False, email="to.delete@example.org")
    user_to_delete.beneficiary_organization_id = user_org.pk
    user_to_delete.save()

    user_org.beneficiaries.add(user_to_delete)
    user_org.save()

    manage_user_content_before_deletion(User, user_to_delete)

    assert Organization.objects.filter(name="Org to delete").count() == 0
