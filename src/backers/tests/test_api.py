import json
import pytest

from django.urls import reverse

from backers.factories import BackerFactory
from aids.models import AidWorkflow
from aids.factories import AidFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_url():
    return reverse("backers-list")


def test_api(client, api_url):
    BackerFactory(name="ADEME")
    BackerFactory(name="Bpifrance")
    BackerFactory(name="DINUM")

    res = client.get(api_url)
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 3


def test_api_with_q_filter(client, api_url):
    BackerFactory(name="ADEME")
    BackerFactory(name="BPI")
    BackerFactory(name="DINUM")

    res = client.get(f"{api_url}?q=ade")
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 1


def test_api_with_financed_aids_filters(client, api_url):
    BackerFactory()
    aid_draft = AidFactory(status=AidWorkflow.states.draft)
    BackerFactory(financed_aids=[aid_draft])
    aid_published_1 = AidFactory(status=AidWorkflow.states.published)
    aid_published_2 = AidFactory(status=AidWorkflow.states.published)
    BackerFactory(financed_aids=[aid_published_1, aid_published_2])

    res = client.get(f"{api_url}?has_financed_aids=true")
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 2

    res = client.get(f"{api_url}?has_published_financed_aids=true")
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 1
