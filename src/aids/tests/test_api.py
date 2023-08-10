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


def test_api_with_version_numbers(client, api_url):
    AidFactory(name="First aid")
    AidFactory(name="Second aid")

    versions = ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]

    for v in versions:
        res = client.get(f"{api_url}?version={v}")
        assert res.status_code == 200
        content = json.loads(res.content.decode())
        assert content["count"] == 2

        if v == "1.0":
            assert "programs" not in content["results"][0]
        elif v == "1.1":
            assert "programs" in content["results"][0]
            assert "categories" not in content["results"][0]
        elif v == "1.2":
            assert "categories" in content["results"][0]
            assert "loan_amount" not in content["results"][0]
            assert "recoverable_advance_amount" not in content["results"][0]
        elif v == "1.3":
            assert "loan_amount" in content["results"][0]
            assert "recoverable_advance_amount" in content["results"][0]
            assert "is_call_for_project" not in content["results"][0]
        elif v == "1.4":
            assert "is_call_for_project" in content["results"][0]
            assert "name_initial" not in content["results"][0]
            assert "import_data_url" not in content["results"][0]
            assert "import_data_mention" not in content["results"][0]
            assert "import_share_licence" not in content["results"][0]
        elif v == "1.5":
            assert "name_initial" in content["results"][0]
            assert "import_data_url" in content["results"][0]
            assert "import_data_mention" in content["results"][0]
            assert "import_share_licence" in content["results"][0]
            assert "is_charged" not in content["results"][0]
        elif v == "1.6":
            assert "is_charged" in content["results"][0]


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
