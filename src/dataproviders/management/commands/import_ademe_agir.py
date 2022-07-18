import requests
from datetime import datetime

from django.conf import settings
from django.utils import timezone

from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify
from dataproviders.management.commands.base import BaseImportCommand


ADMIN_ID = 1

DATA_SOURCE = DataSource.objects.prefetch_related("backer").get(pk=10)


class Command(BaseImportCommand):
    """
    Import data from the Ademe AGIR API.

    Usage:
    python manage.py import_ademe_agir
    """

    def add_arguments(self, parser):
        parser.add_argument("data-file", nargs="?", type=str)

    def handle(self, *args, **options):
        DATA_SOURCE.date_last_access = timezone.now()
        DATA_SOURCE.save()
        super().handle(*args, **options)

    def fetch_data(self, **options):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "client_id": settings.ADEME_AGIR_API_USERNAME,
            "client_secret": settings.ADEME_AGIR_API_PASSWORD,
        }
        req = requests.get(DATA_SOURCE.import_api_url, headers=headers)
        data = req.json()
        self.stdout.write(
            "Total number of aids: {}".format(len(data["ListeDispositifs"]))
        )
        for line in data["ListeDispositifs"]:
            yield line

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        unique_id = "AGIR_{}".format(line["id"])
        return unique_id

    def extract_import_data_url(self, line):
        return DATA_SOURCE.import_data_url

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_import_raw_object(self, line):
        return line

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_name(self, line):
        return line["titre"][:180]

    def extract_name_initial(self, line):
        return line["titre"][:180]

    def extract_description(self, line):
        description = content_prettify(line.get("description_longue", ""))
        return description

    def extract_origin_url(self, line):
        return line["url_agir"]

    def extract_application_url(self, line):
        return line["url_agir"]

    def extract_is_call_for_project(self, line):
        if line.get("type") == "AAP":
            return True
        else:
            return False

    def extract_start_date(self, line):
        start_date = datetime.strptime(line.get("date_debut"), "%Y-%m-%dT%H:%M:%S%z")
        return start_date

    def extract_submission_deadline(self, line):
        submission_deadline = datetime.strptime(
            line.get("date_fin"), "%Y-%m-%dT%H:%M:%S%z"
        )
        return submission_deadline
