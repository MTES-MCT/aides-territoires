import pytest

from backers.models import Backer, BackerCategory, BackerSubCategory, logo_upload_to
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


def test_logo_upload_to():
    backer = BackerFactory(name="Département imaginaire")

    result = logo_upload_to(backer, "0345.png")

    assert result == "backers/departement-imaginaire_logo.png"


def test_backer_category():
    backer_cat = BackerCategory(name="Collectivités")
    backer_cat.save()

    assert backer_cat.id_slug == "1-collectivites"


def test_backer_sub_category():
    backer_cat = BackerCategory(name="Collectivités")
    backer_cat.save()
    backer_subcat = BackerSubCategory(
        name="Conseils départementaux", category=backer_cat
    )
    backer_subcat.save()

    assert backer_subcat.id_slug == "1-conseils-departementaux"
    assert backer_cat == backer_subcat.category
