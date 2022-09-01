import json
import pytest

from django.urls import reverse

from keywords.factories import SynonymListFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_url():
    return reverse("synonymLists-list")


def test_api(client, api_url):
    SynonymListFactory(
        name="Voie douce",
        keywords_list="voie douce, vélo, vélos, liaisons douces, bmx, piste cyclable",
    )
    SynonymListFactory(
        name="Énergie renouvelable",
        keywords_list="biomasse, géothermie, énergie solaire, énergie éolienne",
    )

    res = client.get(api_url)
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 2


def test_api_with_q_filter(client, api_url):
    SynonymListFactory(
        name="Voie douce",
        keywords_list="voie douce, vélo, vélos, liaisons douces, bmx, piste cyclable",
    )
    SynonymListFactory(
        name="Énergie renouvelable",
        keywords_list="biomasse, géothermie, énergie solaire, énergie éolienne",
    )

    res = client.get(f"{api_url}?q=biomasse")
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 1
