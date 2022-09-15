import os
from datetime import datetime
import pytest

from django.core.management import call_command
from django.utils import timezone

from alerts.models import Alert

pytestmark = pytest.mark.django_db


EMAILS_CSV_PATH = os.path.join(os.getcwd(), "alerts/tests/emails.csv")


def test_command_create_default_alerts(mailoutbox):
    call_command("create_alerts_from_csv_file", EMAILS_CSV_PATH)
    assert Alert.objects.count() == 2
    assert len(mailoutbox) == 2


def test_command_create_alerts_with_perimeter(mailoutbox):
    alert_perimeter = "perimeter=70971-nouvelle-aquitaine"
    call_command(
        "create_alerts_from_csv_file", EMAILS_CSV_PATH, querystring=alert_perimeter
    )
    assert Alert.objects.count() == 2
    assert Alert.objects.last().querystring == alert_perimeter
    assert len(mailoutbox) == 2


def test_command_create_alerts_with_title(mailoutbox):
    alert_title = "nom de test"
    call_command("create_alerts_from_csv_file", EMAILS_CSV_PATH, title=alert_title)
    assert Alert.objects.count() == 2
    assert Alert.objects.last().title == alert_title
    assert len(mailoutbox) == 2


def test_command_create_alerts_with_date(mailoutbox):
    alert_latest_alert_date = "2020-08-20"
    call_command(
        "create_alerts_from_csv_file",
        EMAILS_CSV_PATH,
        latest_alert_date=alert_latest_alert_date,
    )
    assert Alert.objects.count() == 2
    assert Alert.objects.last().date_created.date() == timezone.now().date()
    assert (
        Alert.objects.last().latest_alert_date.date()
        == datetime.strptime(alert_latest_alert_date, "%Y-%m-%d").date()
    )  # noqa
    assert len(mailoutbox) == 2


def test_command_create_alerts_with_frequency(mailoutbox):
    alert_frequency = Alert.FREQUENCIES.weekly
    call_command(
        "create_alerts_from_csv_file", EMAILS_CSV_PATH, frequency=alert_frequency
    )
    assert Alert.objects.count() == 2
    assert Alert.objects.last().alert_frequency == alert_frequency
    assert len(mailoutbox) == 2


def test_command_create_alerts_with_validated(mailoutbox):
    call_command("create_alerts_from_csv_file", EMAILS_CSV_PATH, validated=True)
    assert Alert.objects.count() == 2
    assert Alert.objects.last().validated is True
    assert len(mailoutbox) == 0
