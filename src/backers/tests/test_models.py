import pytest

from backers.models import Backer
from backers.factories import BackerFactory
from aids.models import AidWorkflow
from aids.factories import AidFactory


pytestmark = pytest.mark.django_db


def test_backer_slug():
    new_backer = BackerFactory(name="New Backer")

    assert new_backer.slug == "new-backer"


def test_backer_filtering():

    BackerFactory()
    aid_draft = AidFactory(status=AidWorkflow.states.draft)
    BackerFactory(financed_aids=[aid_draft])
    aid_published_1 = AidFactory(status=AidWorkflow.states.published)
    aid_published_2 = AidFactory(status=AidWorkflow.states.published)
    BackerFactory(financed_aids=[aid_published_1, aid_published_2])

    assert Backer.objects.count() == 3
    assert Backer.objects.has_financed_aids().count() == 2
    assert Backer.objects.has_published_financed_aids().count() == 1
