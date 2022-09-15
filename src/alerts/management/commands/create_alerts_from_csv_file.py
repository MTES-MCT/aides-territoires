import os
import csv
from datetime import datetime
import logging

from django.db import transaction
from django.core.management.base import BaseCommand
from django.utils import timezone

from alerts.tasks import send_alert_confirmation_email
from alerts.models import Alert


logger = logging.getLogger(__name__)


DEFAULT_CSV_DELIMITER = ","
DEFAULT_ALERT_QUERYSTRING = ""
DEFAULT_ALERT_VALIDATED = False


class Command(BaseCommand):
    """
    Reusable command to create alerts from a csv file containing a list of emails

    Prerequisites:
    - to follow RGPD, the email users must have given consent beforehand !
    - csv file ? as the first parameter of the command
    - emails ? contained in the csv file, column 'email'
    - querystring ? as an optional parameter of the command

    Usage :
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --querystring 'perimeter=70971-nouvelle-aquitaine' # noqa
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --querystring 'perimeter=70971-nouvelle-aquitaine' --csv_delimiter ';' # noqa
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --querystring 'perimeter=70971-nouvelle-aquitaine' --title 'my custom alert' # noqa
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --querystring 'perimeter=70971-nouvelle-aquitaine' --latest_alert_date '2020-08-20' # noqa
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --querystring 'perimeter=70971-nouvelle-aquitaine' --latest_alert_date '2020-08-20' --frequency weekly # noqa
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --querystring 'perimeter=70971-nouvelle-aquitaine'  --validated # noqa

    CSV File example:
    email
    test@email.com
    test2@email.com
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            nargs=1,
            type=str,
            help="the csv file path. Must have an 'email' column.",
        )
        parser.add_argument(
            "--csv_delimiter",
            nargs="?",
            type=str,
            default=DEFAULT_CSV_DELIMITER,
            help="the csv file delimiter. optional.",
        )
        parser.add_argument(
            "--querystring",
            nargs="?",
            type=str,
            default=None,
            help="the alert querystring. optional.",
        )
        parser.add_argument(
            "--title",
            nargs="?",
            type=str,
            default=None,
            help="the alert title. optional",
        )
        parser.add_argument(
            "--latest_alert_date",
            type=str,
            default=None,
            help="the alert latest alert date. Use format YYY-MM-DD. "
            "The latest alert time will be set to noon. "
            "Useful to define the first reception date. optional.",
        )
        parser.add_argument(
            "--frequency",
            nargs="?",
            type=str,
            choices=Alert.FREQUENCIES,
            default=None,
            help="the alert frequency. optional.",
        )
        parser.add_argument(
            "--validated",
            action="store_true",
            default=DEFAULT_ALERT_VALIDATED,
            help="if the alert is already validated. "
            "If not, it will send a confirmation email. optional.",
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        # csv file
        csv_path = os.path.abspath(options["csv_file"][0])
        csv_delimiter = options["csv_delimiter"]
        # alert details
        alert_querystring = options["querystring"]
        alert_title = options["title"]
        alert_latest_alert_date = options["latest_alert_date"]
        if alert_latest_alert_date:
            alert_latest_alert_date = datetime.strptime(
                options["latest_alert_date"], "%Y-%m-%d"
            ).replace(hour=12, minute=0)
            alert_latest_alert_date = timezone.make_aware(alert_latest_alert_date)
        alert_frequency = options["frequency"]
        alert_validated = options["validated"]

        # build list of alerts
        self.stdout.write("Building the list of alerts...")
        alerts = []
        with open(csv_path) as csv_file:
            csvreader = csv.DictReader(csv_file, delimiter=csv_delimiter)
            if "email" not in csvreader.fieldnames:
                raise KeyError("'email' column missing")
            for index, row in enumerate(csvreader):
                alert = Alert(email=row["email"])
                if alert_querystring:
                    alert.querystring = alert_querystring
                if alert_title:
                    alert.title = alert_title
                if alert_latest_alert_date:
                    alert.latest_alert_date = alert_latest_alert_date
                if alert_frequency:
                    alert.alert_frequency = alert_frequency
                if alert_validated:
                    alert.validate()
                alerts.append(alert)
                self.stdout.write(
                    "Build alert '{}' for {}".format(alert.title, alert.email)
                )

        # create all the alerts simultaneously
        alerts_created = Alert.objects.bulk_create(alerts)

        # send confirmation email
        alerts_created_not_validated = [
            alert for alert in alerts_created if not alert.validated
        ]  # noqa
        self.stdout.write(
            "Sending validation emails for {} alerts".format(
                len(alerts_created_not_validated)
            )
        )
        for alert in alerts_created_not_validated:
            send_alert_confirmation_email.delay(alert.email, alert.token)

        self.stdout.write(
            self.style.SUCCESS("Done! %d alerts created." % (len(alerts_created)))
        )
