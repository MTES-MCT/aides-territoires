import os
import csv
import datetime
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from alerts.tasks import send_alert_confirmation_email
from alerts.models import Alert


logger = logging.getLogger(__name__)


DEFAULT_CSV_DELIMITER = ','
DEFAULT_ALERT_QUERYSTRING = ''
DEFAULT_ALERT_TITLE = 'Alerte'
DEFAULT_ALERT_FREQUENCY = Alert.FREQUENCIES.daily
DEFAULT_ALERT_VALIDATED = False


class Command(BaseCommand):
    """
    Reusable command to create alerts from a csv file containing a list of emails

    - csv file ? as the first parameter of the command
    - emails ? contained in the csv file, column 'email'
    - querystring ? as an optional parameter of the command

    Usage :
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --alert_querystring 'perimeter=70971-nouvelle-aquitaine' # noqa
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --alert_querystring 'perimeter=70971-nouvelle-aquitaine' --alert_title 'my custom alert' # noqa
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --alert_querystring 'perimeter=70971-nouvelle-aquitaine' --alert_date_created '2020-08-20' # noqa
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --alert_querystring 'perimeter=70971-nouvelle-aquitaine' --alert_date_created '2020-08-20 2:00' --alert_frequency weekly # noqa
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --alert_querystring 'perimeter=70971-nouvelle-aquitaine'  --alert_validated # noqa

    CSV File example:
    email
    test@email.com
    test2@email.com
    """

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=str)
        parser.add_argument(
            '--csv_delimiter', nargs='?', type=str,
            default=DEFAULT_CSV_DELIMITER
        )
        parser.add_argument(
            '--alert_querystring', nargs='?', type=str,
            default=DEFAULT_ALERT_QUERYSTRING
        )
        parser.add_argument(
            '--alert_title', nargs='?', type=str,
            default=DEFAULT_ALERT_TITLE
        )
        parser.add_argument(
            '--alert_date_created', type=datetime.datetime.fromisoformat,
            default=timezone.now()
        )
        parser.add_argument(
            '--alert_frequency', nargs='?', type=str,
            choices=Alert.FREQUENCIES, default=DEFAULT_ALERT_FREQUENCY
        )
        parser.add_argument(
            '--alert_validated', action='store_true',
            default=DEFAULT_ALERT_VALIDATED
        )

    def handle(self, *args, **options):
        # csv file
        csv_path = os.path.abspath(options['csv_file'][0])
        csv_delimiter = options['csv_delimiter']
        # alert details
        alert_querystring = options['alert_querystring']
        alert_title = options['alert_title']
        alert_date_created = options['alert_date_created']
        alert_frequency = options['alert_frequency']
        alert_validated = options['alert_validated']

        with open(csv_path) as csv_file:
            csvreader = csv.DictReader(csv_file, delimiter=csv_delimiter)
            for index, row in enumerate(csvreader):
                self.create_alert(row['email'], alert_querystring, alert_title, alert_date_created, alert_frequency, alert_validated) # noqa

    def create_alert(self, alert_email, alert_querystring, alert_title, alert_date_created, alert_frequency, alert_validated): # noqa
        print(alert_date_created)
        alert = Alert.objects.create(
            email=alert_email,
            querystring=alert_querystring,
            title=alert_title,
            alert_frequency=alert_frequency,
            date_created=alert_date_created,
        )

        self.stdout.write('Alert {} created for {}'.format(
            alert.title, alert.email))

        # send confirmation email
        if alert_validated:
            alert.validate()
            alert.save()
        else:
            send_alert_confirmation_email.delay(alert.email, alert.token)
