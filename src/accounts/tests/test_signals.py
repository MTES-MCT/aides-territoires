import pytest

from accounts.models import User
from accounts.signals import manage_user_content_before_deletion
from aids.factories import AidFactory
from accounts.factories import UserFactory
from geofr.models import Perimeter
from organizations.models import Organization
from projects.factories import ProjectFactory

pytestmark = pytest.mark.django_db


def test_manage_user_content_before_deletion_is_set(client):

    user_org = Organization(name="Sample Org", perimeter=Perimeter.objects.first())
    user_org.save()

    user_to_delete = UserFactory(is_contributor=False, email="to.delete@example.org")
    user_to_delete.beneficiary_organization_id = user_org.pk
    user_to_delete.save()

    other_user = UserFactory(is_contributor=False, email="to.keep@example.org")
    other_user.beneficiary_organization_id = user_org.pk
    other_user.save()

    project_to_reattribute = ProjectFactory(name="Stroumpfer les aides")
    manage_user_content_before_deletion(User, user_to_delete)

    assert project_to_reattribute.author.email == other_user.email
