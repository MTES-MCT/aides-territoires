import pytest

from django.urls import reverse
from django.utils import timezone

from alerts.models import Alert
from alerts.factories import AlertFactory
from geofr.factories import PerimeterFactory
from accounts.models import User
from search.factories import SearchPageFactory


pytestmark = pytest.mark.django_db


def test_anonymous_can_create_a_alert(client, mailoutbox):
    """Anonymous can create alerts. They receive a validation email."""

    alerts = Alert.objects.all()
    assert alerts.count() == 0

    users = User.objects.all()
    assert users.count() == 0

    url = reverse("alert_create_view")
    res = client.post(
        url,
        data={
            "title": "My new search",
            "email": "alert-user@example.com",
            "alert_frequency": "daily",
            "querystring": "text=Ademe&call_for_projects_only=on",
            "source": "aides-territoires",
        },
    )
    assert res.status_code == 302
    assert alerts.count() == 1
    assert users.count() == 0

    alert = alerts[0]
    assert alert.email == "alert-user@example.com"
    assert alert.title == "My new search"
    assert "text=Ademe" in alert.querystring
    assert "call_for_projects_only=on" in alert.querystring
    assert not alert.validated
    assert alert.date_validated is None

    assert len(mailoutbox) == 1


def test_anonymous_can_create_several_alerts(client, mailoutbox):
    """Anonymous can create several alerts.

    As long as they don't validate their email, we don't require for them
    to log in. Otherwise, it would prevent them to create several alerts
    at once.
    """
    alerts = Alert.objects.order_by("date_created")
    assert alerts.count() == 0

    users = User.objects.all()
    assert users.count() == 0

    url = reverse("alert_create_view")
    res = client.post(
        url,
        data={
            "title": "My new search",
            "email": "alert-user@example.com",
            "alert_frequency": "daily",
            "querystring": "text=Ademe&call_for_projects_only=on",
            "source": "aides-territoires",
        },
    )
    assert res.status_code == 302
    assert alerts.count() == 1
    assert users.count() == 0

    res = client.post(
        url,
        data={
            "title": "My new search 2",
            "email": "alert-user@example.com",
            "alert_frequency": "daily",
            "querystring": "text=Ademe&call_for_projects_only=off",
            "source": "aides-territoires",
        },
    )
    assert res.status_code == 302
    assert alerts.count() == 2
    assert users.count() == 0

    alert = alerts[1]
    assert alert.email == "alert-user@example.com"
    assert alert.title == "My new search 2"

    # We send validation email for every alert
    assert len(mailoutbox) == 2


def test_anonymous_have_a_connect_message_in_the_modale(client):
    """The button is only present for anonymous users on portals, not the main site"""
    url = reverse("search_view")
    res = client.get(url)
    assert (
        "Connectez-vous pour être notifié des nouvelles aides" in res.content.decode()
    )


def test_logged_user_have_the_alert_creation_in_the_modale(client, contributor):
    client.force_login(contributor)
    url = reverse("search_view")
    res = client.get(url)
    assert (
        "En créant une alerte, vous acceptez que vos données soient traitées"
        in res.content.decode()
    )


def test_alert_perimeter(client, mailoutbox):
    """The search perimeter is displayed in the validation email."""

    perimeter = PerimeterFactory.create(name="Bretagne")
    perimeter_id = "{}-{}".format(perimeter.id, perimeter.code)
    url = reverse("alert_create_view")
    res = client.post(
        url,
        data={
            "title": "Test",
            "email": "alert-user@example.com",
            "alert_frequency": "daily",
            "querystring": "text=Ademe&perimeter={}".format(perimeter_id),
            "source": "aides-territoires",
        },
    )
    assert res.status_code == 302
    assert len(mailoutbox) == 1
    assert perimeter_id in Alert.objects.last().querystring


def test_alert_from_search_page(client, mailoutbox):
    """The search perimeter is displayed in the validation email."""

    perimeter = PerimeterFactory.create(name="Bretagne")
    perimeter_id = "{}-{}".format(perimeter.id, perimeter.code)
    page = SearchPageFactory(
        title="Minisite", search_querystring="perimeter={}".format(perimeter_id)
    )
    url = reverse("alert_create_view")
    res = client.post(
        url,
        data={
            "title": "Test",
            "email": "alert-user@example.com",
            "alert_frequency": "daily",
            "querystring": "",
            "source": page.slug,
        },
    )
    assert res.status_code == 302
    assert len(mailoutbox) == 1
    assert perimeter_id in Alert.objects.last().querystring


def test_unvalidated_alerts_creation_quotas(client):
    """There is a maximum amount of unvalidated alerts one can create."""

    AlertFactory.create_batch(10, validated=False, email="alert-user@example.com")

    alerts = Alert.objects.all()
    assert alerts.count() == 10

    url = reverse("alert_create_view")
    res = client.post(
        url,
        data={
            "title": "My new search",
            "email": "alert-user@example.com",
            "alert_frequency": "daily",
            "querystring": "text=Ademe&call_for_projects_only=on",
            "source": "aides-territoires",
        },
    )
    assert res.status_code == 302
    assert alerts.count() == 10


def test_alert_creation_quotas(client):
    """There is a maximum amount of alerts one can create."""

    AlertFactory.create_batch(100, email="alert-user@example.com")

    alerts = Alert.objects.all()
    assert alerts.count() == 100

    url = reverse("alert_create_view")
    res = client.post(
        url,
        data={
            "title": "My new search",
            "email": "alert-user@example.com",
            "alert_frequency": "daily",
            "querystring": "text=Ademe&call_for_projects_only=on",
            "source": "aides-territoires",
        },
    )
    assert res.status_code == 302
    assert alerts.count() == 100


def test_alert_validation_url(client):
    alert = AlertFactory(validated=False, date_validated=None)
    assert not alert.validated
    assert alert.date_validated is None

    validation_url = reverse("alert_validate_view", args=[alert.token])
    res = client.get(validation_url)
    assert res.status_code == 200

    alert.refresh_from_db()
    assert not alert.validated

    res = client.post(validation_url)
    alert.refresh_from_db()
    assert res.status_code == 302
    assert alert.validated
    assert alert.date_validated.date() == timezone.now().date()


def test_delete_alert(client):
    alerts = Alert.objects.all()

    alert = AlertFactory()
    url = reverse("alert_delete_view", args=[alert.token])
    res = client.get(url)
    assert res.status_code == 200
    assert alerts.count() == 1

    res = client.post(url)
    assert res.status_code == 302
    assert alerts.count() == 0
