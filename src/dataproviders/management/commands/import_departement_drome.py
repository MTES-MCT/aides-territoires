# flake8: noqa
import os
import csv
import json
import requests

from django.utils import timezone

from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import get_category_list_from_name
from dataproviders.management.commands.base import BaseImportCommand
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid

ADMIN_ID = 1

DATA_SOURCE = DataSource.objects.prefetch_related("perimeter", "backer").get(pk=9)

OPENDATA_URL = "https://www.ladrome.fr/"
FEED_ROWS = 1000


class Command(BaseImportCommand):
    """
    Import data from the Conseil Départemental de la Drôme Data plateform.
    """

    def add_arguments(self, parser):
        parser.add_argument("data-file", nargs="?", type=str)

    def handle(self, *args, **options):
        DATA_SOURCE.date_last_access = timezone.now()
        DATA_SOURCE.save()
        super().handle(*args, **options)

    def fetch_data(self, **options):
        if options["data-file"]:
            data_file = os.path.abspath(options["data-file"])
            data = json.load(open(data_file))
            for line in data["data"]:
                yield line
        else:
            req = requests.get(DATA_SOURCE.import_api_url)
            req.encoding = (
                "utf-8-sig"  # We need this to take care of the bom (byte order mark)
            )
            data = json.loads(req.text)
            self.stdout.write("Total number of aids: {}".format(data["count"]))
            if data["count"] > FEED_ROWS:
                self.stdout.write(
                    self.style.ERROR(
                        "Only fetching {} aids, but there are {} aids".format(
                            FEED_ROWS, data["count"]
                        )
                    )
                )
            self.stdout.write(
                "Number of aids processing: {}".format(len(data["results"]))
            )
            for line in data["results"]:
                yield line

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        unique_id = "CDDr_{}".format(line["name"][:180])
        return unique_id

    def extract_import_data_url(self, line):
        return ""

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_import_raw_object_calendar(self, line):
        import_raw_object_calendar = {}
        if line.get("start_date", None) != None:
            import_raw_object_calendar["start_date"] = line["start_date"]
        if line.get("predeposit_date", None) != None:
            import_raw_object_calendar["predeposit_date"] = line["predeposit_date"]
        if line.get("submission_deadline", None) != None:
            import_raw_object_calendar["submission_deadline"] = line[
                "submission_deadline"
            ]
        if line.get("recurrence", None) != None:
            import_raw_object_calendar["recurrence"] = line["recurrence"]
        return import_raw_object_calendar

    def extract_import_raw_object(self, line):
        import_raw_object = dict(line)
        if line.get("start_date", None) != None:
            import_raw_object.pop("start_date")
        if line.get("predeposit_date", None) != None:
            import_raw_object.pop("predeposit_date")
        if line.get("submission_deadline", None) != None:
            import_raw_object.pop("submission_deadline")
        if line.get("recurrence", None) != None:
            import_raw_object.pop("recurrence")
        return import_raw_object

    def extract_recurrence(self, line):
        if line.get("recurrence", None) != None:
            if line.get("recurrence") == 'Permanente':
                recurrence = Aid.RECURRENCES.ongoing
            if line.get("recurrence") == 'Ponctuelle':
                recurrence = Aid.RECURRENCES.oneoff
            if line.get("recurrence") == 'Récurrente':
                recurrence = Aid.RECURRENCES.recurring
        return recurrence

    def extract_name(self, line):
        name = line["name"][:180]
        return name

    def extract_name_initial(self, line):
        name_initial = line["name"][:180]
        return name_initial

    def extract_description(self, line):
        description = line["description"]
        return description

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_origin_url(self, line):
        origin_url = line["origin_url"]
        return origin_url

    def extract_application_url(self, line):
        application_url = line["application_url"]
        return application_url

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process: ["Communes", "Associations"]
        """
        if line.get("targeted_audiences", None) != None:
            audiences = line.get("targeted_audiences", None)
            aid_audiences = []
            for audience in audiences:
                aid_audiences.extend(audience)
            return aid_audiences
        else:
            return []

    def extract_aid_types(self, line):
        """
        Exemple of string to process: "Appel à propositions"
        """
        types = line.get("aid_types", None)
        aid_types = []
        for type_item in types:
            aid_types.extend(type_item)
        return aid_types

    def extract_is_call_for_project(self, line):
        is_call_for_project = True
        return is_call_for_project

    def extract_start_date(self, line):
        if line.get("start_date", None) != None:
            start_date = line.get("start_date", None)
            return start_date

    def extract_submission_deadline(self, line):
        if line.get("submission_deadline", None) != None:
            submission_deadline = line.get("submission_deadline", None)
            return submission_deadline

    def extract_categories(self, line):
        """
        Exemple of string to process: [
                "B\u00e2timents et construction",
                "Foncier",
                "Logement et habitat",
                "Equipement public",
                "Voirie"
            ]
        """
        categories = line.get("categories", None)
        name = line["name"][:180]
        aid_categories = []
        if categories != []:
            for category in categories:
                try:
                    get_category_list_from_name(category)
                    aid_categories.extend(get_category_list_from_name(category))
                except Exception:
                    print(f"{category}")
        else:
            print(f"{title} aucune thématique")
        return aid_categories

    def extract_contact(self, line):
        if line.get("contact", None) != None:
            contact = line.get("contact")
        return contact
