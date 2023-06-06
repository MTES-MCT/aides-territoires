import pytest

from django.core.management import call_command

from aids.factories import AidFactory
from alerts.factories import AlertFactory
from search.factories import SearchPageFactory

pytestmark = pytest.mark.django_db


def test_command_with_no_alerts(mailoutbox):
    call_command("send_alerts")
    assert len(mailoutbox) == 0


def test_command_with_an_alert_but_no_aids(mailoutbox):
    AlertFactory(querystring="text=Schtroumpf")
    call_command("send_alerts")
    assert len(mailoutbox) == 0


def test_command_with_an_alert_but_no_matching_aids(mailoutbox):
    AlertFactory(querystring="text=Schtroumpf")
    AidFactory.create_batch(5, name="Gloubiboulga")
    call_command("send_alerts")
    assert len(mailoutbox) == 0


def test_command_with_matching_aids(mailoutbox):
    search_page = SearchPageFactory(slug="martinique")
    alert = AlertFactory(querystring="text=Schtroumpf", source=search_page.slug)
    AidFactory.create_batch(5, name="Schtroumpf")
    call_command("send_alerts")
    assert len(mailoutbox) == 1
    assert list(mailoutbox[0].to) == [alert.email]


def test_command_with_unvalidated_address(mailoutbox):
    AlertFactory(validated=False, querystring="text=Schtroumpf")
    AidFactory.create_batch(5, name="Schtroumpf")
    call_command("send_alerts")
    assert len(mailoutbox) == 0


def test_command_output_format(mailoutbox):
    AlertFactory(
        title="Gloubiboukmark",
        querystring="text=Schtroumpf",
        source="aides-territoires",
    )
    AidFactory.create(name="Schtroumpf 1")
    AidFactory.create(name="Schtroumpf 2")
    AidFactory.create(name="Schtroumpf 3")
    AidFactory.create(name="Schtroumpf 4")
    call_command("send_alerts")

    content = mailoutbox[0].body
    assert "Gloubiboukmark" in content
    assert "Schtroumpf 1" in content
    assert "Schtroumpf 2" in content
    assert "Schtroumpf 3" in content

    # Only the first three aids are in the mail
    assert "Schtroumpf 4" not in content
    assert "encore d’autres aides disponibles !" in content

    # The "extra search" link should include these parameters
    assert "published_after=" in content
    assert "action=alert" in content
