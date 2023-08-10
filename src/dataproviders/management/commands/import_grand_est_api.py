import os
import csv
import json
import requests
from datetime import datetime

from django.conf import settings
from django.utils import timezone

from aids.constants import ALL_FINANCIAL_AIDS, TECHNICAL_AIDS
from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify, mapping_categories
from dataproviders.management.commands.base import BaseImportCommand
from aids.models import Aid
from programs.models import Program


ADMIN_ID = 1

DATA_SOURCE = DataSource.objects.prefetch_related("perimeter", "backer").get(pk=3)

AUDIENCES_DICT = {}
AUDIENCES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/grand_est_api_audiences_mapping.csv"
)
SOURCE_COLUMN_NAME = "Bénéficiaires Grand Est"
AT_COLUMN_NAMES = [
    "Bénéficiaires AT 1",
    "Bénéficiaires AT 2",
    "Bénéficiaires AT 3",
    "Bénéficiaires AT 4",
]
with open(AUDIENCES_MAPPING_CSV_PATH) as csv_file:
    csvreader = csv.DictReader(csv_file, delimiter=",")
    for index, row in enumerate(csvreader):
        if row[AT_COLUMN_NAMES[0]]:
            AUDIENCES_DICT[row[SOURCE_COLUMN_NAME]] = []
            for column in AT_COLUMN_NAMES:
                if row[column]:
                    try:
                        audience = next(
                            choice[0]
                            for choice in Aid.AUDIENCES
                            if choice[1] == row[column]
                        )
                        AUDIENCES_DICT[row[SOURCE_COLUMN_NAME]].append(audience)
                    except:  # noqa NOSONAR
                        print(row[column])

CATEGORIES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/grand_est_api_categories_mapping.csv"
)
SOURCE_COLUMN_NAME = "Sous-thématiques Grand Est"  # 'Thématiques Grand Est'
AT_COLUMN_NAMES = [
    "Sous-thématiques AT 1",
    "Sous-thématiques AT 2",
    "Sous-thématiques AT 3",
    "Sous-thématiques AT 4",
    "Sous-thématiques AT 5",
    "Sous-thématiques AT 6",
    "Sous-thématiques AT 7",
    "Sous-thématiques AT 8",
]
CATEGORIES_DICT = mapping_categories(
    CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES
)


class Command(BaseImportCommand):
    """
    Import data from the Grand Est API.
    219 aids as of May 2021
    258 aids as of May 2023

    Usage:
    python manage.py import_grand_est_api
    python manage.py import_grand_est_api grand-est.json

    Note:
    If your access to the json file is only accessible through an IPv4
    connection, there is a shell script to force this:

    sh scripts/dataproviders/grand_est_download_json.sh
    python manage.py import_grand_est_api /tmp/aides-regionales.json

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
            self.stdout.write(f"Total number of aids: {len(data)}")
            for line in data:
                yield line
        else:
            headers = {"accept": "application/json", "content-type": "application/json"}
            req = requests.get(
                DATA_SOURCE.import_api_url,
                headers=headers,
                auth=(settings.GRAND_EST_API_USERNAME, settings.GRAND_EST_API_PASSWORD),
            )
            data = req.json()
            self.stdout.write(f"Total number of aids: {len(data)}")
            for line in data:
                yield line

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        return line["ID"]

    def extract_import_data_url(self, line):
        return DATA_SOURCE.import_data_url

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_import_raw_object_calendar(self, line):
        import_raw_object_calendar = {}
        if line.get("pro_fin", None) is not None:
            import_raw_object_calendar["pro_fin"] = line["pro_fin"]
        if line.get("post_date", None) is not None:
            import_raw_object_calendar["post_date"] = line["post_date"]
        return import_raw_object_calendar

    def extract_import_raw_object(self, line):
        import_raw_object = dict(line)
        if line.get("pro_fin", None) is not None:
            import_raw_object.pop("pro_fin")
        if line.get("post_date", None) is not None:
            import_raw_object.pop("post_date")

        return import_raw_object

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_name(self, line):
        return line["post_title"][:180]

    def extract_description(self, line):
        # desc_1 = content_prettify(line.get('gui_introduction', ''))
        description = content_prettify(line.get("post_content", ""))
        # description = desc_1 + desc_2
        return description

    def extract_destinations(self, line):
        """
        Source format: list of strings
        These strings match our values from Aid.DESTINATIONS, so we just have
        to revert the dict to get the key
        """
        DESTINATIONS_DICT = {v: k for k, v in dict(Aid.DESTINATIONS).items()}
        aid_destinations = []

        destinations = line.get("gui_actions_concernees", [])
        for destination in destinations:
            aid_destinations.append(DESTINATIONS_DICT[destination])

        return aid_destinations

    def extract_aid_types(self, line):
        """
        Source format: list of dicts
        Get the objects, loop on the values and match to our AID_TYPES
        """
        post_type = line.get("post_type")

        if post_type == "ge_guide":
            # Aides régionales
            financial_aid_types_field = "gui_nature_aide_financieres"
            technical_aid_types_field = "gui_nature_aide_ingenierie"
        else:
            # Appels à projets (AAP)
            financial_aid_types_field = "pro_nature_aide_financieres"
            technical_aid_types_field = "pro_nature_aide_ingenierie"

        aid_types = []

        financial_aid_types = line.get(financial_aid_types_field, [])
        for aid_type_label in financial_aid_types:
            aid_type = [
                item[0] for item in ALL_FINANCIAL_AIDS if item[1] == aid_type_label
            ][0]
            if aid_type:
                aid_types.append(aid_type)
            else:
                self.stdout.write(
                    self.style.ERROR(f"Aid type {aid_type_label} not mapped")
                )

        technical_aid_types = line.get(technical_aid_types_field, [])
        for aid_type_label in technical_aid_types:
            aid_type = [
                item[0] for item in TECHNICAL_AIDS if item[1] == aid_type_label
            ][0]
            if aid_type:
                aid_types.append(aid_type)
            else:
                self.stdout.write(
                    self.style.ERROR(f"Aid type {aid_type_label} not mapped")
                )

        return aid_types

    def extract_targeted_audiences(self, line):
        """
        Source format: list of dicts
        Get the objects, loop on the values and match to our AUDIENCES
        """
        audiences = line.get("gui_beneficiaire", [])
        aid_audiences = []
        for audience in audiences:
            audience_name = audience["name"]
            if audience_name in AUDIENCES_DICT:
                aid_audiences.extend(AUDIENCES_DICT.get(audience_name, []))
            else:
                self.stdout.write(
                    self.style.ERROR(f"Audience {audience_name} not mapped")
                )
                # self.stdout.write(self.style.ERROR(f'{audience_name}'))
        return aid_audiences

    def extract_programs(self, line):
        """
        Source format: list of ints
        Get the objects, loop on the values and match to our AUDIENCES
        Exemple of string to process:
        "FEDER - Fonds européen de développement régional"
        They use AT's program names, minus the EU flag emoji (🇪🇺)
        some of our programs names have
        """
        programs = line.get("gui_programme_aides", [])
        aid_programs = []
        if programs != [""]:
            for program in programs:
                at_program = Program.objects.filter(name__contains=program).first()

                if at_program:
                    aid_programs.append(at_program)

        return aid_programs

    def extract_categories(self, line):
        """
        Source format: list of dicts
        Get the objects, loop on the values and match to our Categories
        """
        categories = line.get("gui_tax_competence", [])
        aid_categories = []
        for category in categories:
            category_name = category["name"]
            if category_name in CATEGORIES_DICT:
                aid_categories.extend(CATEGORIES_DICT.get(category_name, []))
            else:
                self.stdout.write(
                    self.style.ERROR(f"Category {category_name} not mapped")
                )
                # self.stdout.write(self.style.ERROR(f'{category_name}'))
        return aid_categories

    def extract_origin_url(self, line):
        return line["url"]

    def extract_contact(self, line):
        return line.get("gui_texte_gris", "")

    def extract_application_url(self, line):
        return line["gui_dematerialise_url"]

    def extract_mobilization_steps(self, line):
        return [Aid.STEPS.op]

    def extract_is_call_for_project(self, line):
        return line.get("post_type") == "ge_projet"

    def extract_recurrence(self, line):
        is_call_for_project = line.get("post_type") == "ge_projet"
        if is_call_for_project:
            return Aid.RECURRENCES.oneoff
        return Aid.RECURRENCES.ongoing

    def extract_start_date(self, line):
        is_call_for_project = line.get("post_type") == "ge_projet"
        if is_call_for_project:
            start_date = datetime.strptime(line.get("post_date"), "%Y-%m-%d %H:%M:%S")
            return start_date

    def extract_submission_deadline(self, line):
        is_call_for_project = line.get("post_type") == "ge_projet"
        if is_call_for_project:
            start_date = datetime.strptime(line.get("pro_fin"), "%Y-%m-%d")
            return start_date
