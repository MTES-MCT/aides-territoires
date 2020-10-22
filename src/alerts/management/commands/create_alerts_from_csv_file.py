import os
import csv
import logging

from django.core.management.base import BaseCommand

from alerts.tasks import send_alert_confirmation_email
from alerts.models import Alert


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Create alerts from a csv file

    - csv file ? as the first parameter of the command
    - emails ? contained in the csv file, column 'email'
    - querystring ? as the second parameter of the command

    Usage : 
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --alert_querystring 'query=test'
    pipenv run python manage.py create_alerts_from_csv_file file/path/name.csv --alert_querystring '?query=test' --alert_title 'my custom alert' --alert_frequency weekly --alert_validated

    TODO: 
    - comment définir un envoi "dans la nuit de jeudi à vendredi" ?
    - validated = True or False ? si False envoyer email de confirmation send_alert_confirmation_email.delay(alert.email, alert.token)
    """

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=str)
        parser.add_argument('--csv_delimiter', nargs='?', type=str, default=',')
        parser.add_argument('--alert_querystring', nargs='?', type=str, default='')
        parser.add_argument('--alert_title', nargs='?', type=str, default='alerte')
        parser.add_argument('--alert_frequency', nargs='?', type=str, choices=Alert.FREQUENCIES, default=Alert.FREQUENCIES.daily)
        parser.add_argument('--alert_validated', action='store_true', default=False)

    def handle(self, *args, **options):
        print(options)
        # csv file
        csv_path = os.path.abspath(options['csv_file'][0])
        csv_delimiter = options['csv_delimiter']
        # alert details
        alert_querystring = options['alert_querystring']
        alert_title = options['alert_title']
        alert_frequency = options['alert_frequency']
        alert_validated = options['alert_validated']

        with open(csv_path) as csv_file:
            csvreader = csv.DictReader(csv_file, delimiter=csv_delimiter)
            for index, row in enumerate(csvreader):
                # if index < 1:
                #     print(row['email'])
                self.create_alert(row['email'], alert_querystring, alert_title, alert_frequency, alert_validated)

    def create_alert(self, alert_email, alert_querystring, alert_title, alert_frequency, alert_validated):
        alert = Alert.objects.create(
            email=alert_email,
            querystring=alert_querystring,
            title=alert_title,
            alert_frequency=alert_frequency,
            validated=alert_validated
        )
        if not alert.validated:
            send_alert_confirmation_email.delay(alert.email, alert.token)
