import json
import pytest
from django.urls import reverse

from aids.factories import AidFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_url():
    return reverse("aids-list")


def test_api_default_version(client, api_url):
    AidFactory(name="First aid")
    AidFactory(name="Second aid")

    res = client.get(api_url)
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 2


def test_api_version_1_0(client, api_url):
    AidFactory(name="First aid")
    AidFactory(name="Second aid")

    res = client.get(f"{api_url}?version=1.0")
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 2
    assert "programs" not in content["results"][0]


def test_api_version_1_1(client, api_url):
    AidFactory(name="First aid")
    AidFactory(name="Second aid")

    res = client.get(f"{api_url}?version=1.1")
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 2
    assert "programs" in content["results"][0]


def test_api_invalid_version(client, api_url):
    AidFactory(name="First aid")
    AidFactory(name="Second aid")

    res = client.get("f{api_url}?version=42")
    assert res.status_code == 404


def test_superuser_can_search_among_aid_drafts(superuser_client, api_url):
    AidFactory(name="First aid")
    AidFactory(name="Draft aid", status="draft")

    res = superuser_client.get(f"{api_url}?version=1.1")
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 1

    res = superuser_client.get(f"{api_url}?version=1.1&drafts=True")
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 2


def test_users_cannot_search_among_aid_drafts(user_client, api_url):
    AidFactory(name="First aid")
    AidFactory(name="Draft aid", status="draft")

    res = user_client.get(f"{api_url}?version=1.1")
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 1

    res = user_client.get(f"{api_url}?version=1.1&drafts=True")
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["count"] == 1
