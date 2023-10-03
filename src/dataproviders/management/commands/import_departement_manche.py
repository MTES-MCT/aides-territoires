import json
import os
import requests
from datetime import datetime

from django.conf import settings
from django.utils import timezone

from aids.models import Aid
from keywords.models import Keyword
from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import (
    content_prettify,
    mapping_categories,
)
from dataproviders.management.commands.base import BaseImportCommand

ADMIN_ID = 1

DATA_SOURCE = DataSource.objects.prefetch_related("backer").get(pk=12)

CATEGORIES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/departement_manche_categories_mapping.csv"
)
SOURCE_COLUMN_NAME = "Sous-thématique du Conseil départemental de la Manche"
AT_COLUMN_NAMES = [
    "Sous-thématique AT 1",
    "Sous-thématique AT 2",
    "Sous-thématique AT 3",
]
CATEGORIES_DICT = mapping_categories(
    CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES
)


class Command(BaseImportCommand):
    """
    Import data from the Conseil Départemantal de la Manche API.

    Usage:
    python manage.py import_departement_manche
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
            aids_count = len(data["aides"])
            self.stdout.write(f"Total number of aids: {aids_count}")
            for line in data["aides"]:
                yield line
        else:
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
            }
            req = requests.get(
                DATA_SOURCE.import_api_url,
                headers=headers,
                auth=(settings.MANCHE_API_USERNAME, settings.MANCHE_API_PASSWORD),
            )
            data = req.json()
            self.stdout.write("Total number of aids: {}".format(len(data["aides"])))
            for line in data["aides"]:
                yield line

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_data_mention(self, line):
        return "Ces données sont mises à disposition par le Conseil départemental de la Manche."

    def extract_import_uniqueid(self, line):
        unique_id = "CDManche_{}".format(line["id"])
        return unique_id

    def extract_import_data_url(self, line):
        return DATA_SOURCE.import_data_url

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_import_raw_object_calendar(self, line):
        import_raw_object_calendar = {}
        if line.get("start_date", None) is not None:
            import_raw_object_calendar["start_date"] = line["start_date"]
        if line.get("predeposit_date", None) is not None:
            import_raw_object_calendar["predeposit_date"] = line["predeposit_date"]
        if line.get("submission_deadline", None) is not None:
            import_raw_object_calendar["submission_deadline"] = line[
                "submission_deadline"
            ]
        if line.get("recurrence", None) is not None:
            import_raw_object_calendar["recurrence"] = line["recurrence"]
        return import_raw_object_calendar

    def extract_import_raw_object(self, line):
        import_raw_object = dict(line)
        if line.get("start_date", None) is not None:
            import_raw_object.pop("start_date")
        if line.get("predeposit_date", None) is not None:
            import_raw_object.pop("predeposit_date")
        if line.get("submission_deadline", None) is not None:
            import_raw_object.pop("submission_deadline")
        if line.get("recurrence", None) is not None:
            import_raw_object.pop("recurrence")
        return import_raw_object

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_name(self, line):
        return line["name"][:180]

    def extract_name_initial(self, line):
        return line["name"][:180]

    def extract_description(self, line):
        description = content_prettify(line.get("description", ""))
        return description

    def extract_origin_url(self, line):
        if line.get("origin_url", None) is not None:
            return line["origin_url"]
        else:
            return ""

    def extract_application_url(self, line):
        if line.get("application_url", None) is not None:
            return line.get("application_url")
        else:
            return ""

    def extract_is_call_for_project(self, line):
        is_call_for_project = line.get("is_call_for_project", False)
        return is_call_for_project

    def extract_aid_types(self, line):
        aid_types = line.get("aid_types", None)
        name = line["name"][:180]
        aid_aid_types = []
        if aid_types is not None and aid_types != []:
            for aid_type in aid_types:
                try:
                    aid_type_key = next(
                        choice[0] for choice in Aid.TYPES if choice[1] == aid_type
                    )
                    aid_aid_types.append(aid_type_key)
                except Exception:
                    print(aid_type_key)
        else:
            print(f"{name} aucun bénéficiaire")
        return aid_aid_types

    def extract_start_date(self, line):
        if line.get("start_date", None) is not None:
            start_date = datetime.strptime(
                line.get("start_date"), "%Y-%m-%dT%H:%M:%S%z"
            )
            return start_date

    def extract_submission_deadline(self, line):
        if line.get("submission_deadline", None) is not None:
            submission_deadline = datetime.strptime(
                line.get("submission_deadline"), "%Y-%m-%dT%H:%M:%S%z"
            )
            return submission_deadline

    def extract_recurrence(self, line):
        if line.get("recurrence", None) is not None:
            recurrence = line.get("recurrence")
            if recurrence == "Ponctuelle":
                return Aid.RECURRENCES.oneoff
            elif recurrence == "Permanente":
                return Aid.RECURRENCES.ongoing
            elif recurrence == "Récurrente":
                return Aid.RECURRENCES.recurring
            else:
                return []

    def extract_mobilization_steps(self, line):
        return [Aid.STEPS.op, Aid.STEPS.preop, Aid.STEPS.postop]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_eligibility(self, line):
        eligibility = line.get("eligibility", "")
        return eligibility

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process:
        [
            "Communes",
            "Intercommunalités / Pays",
            "Associations",
            "Particuliers"
        ]
        """
        targeted_audiences = line.get("targeted_audiences", None)
        name = line["name"][:180]
        aid_targeted_audiences = []
        if targeted_audiences is not None and targeted_audiences != []:
            for targeted_audience in targeted_audiences:
                """
                Mostly matches our audiences save for two, so mapping manually here
                """
                if (
                    targeted_audience
                    == "Établissements publics (écoles, bibliothèques…)"
                ):
                    aid_targeted_audiences.append("public_org")
                elif targeted_audience == "EPCI à fiscalité propre":
                    aid_targeted_audiences.append("epci")
                else:
                    try:
                        targeted_audience = next(
                            choice[0]
                            for choice in Aid.AUDIENCES
                            if choice[1] == targeted_audience
                        )
                        aid_targeted_audiences.append(targeted_audience)
                    except Exception:
                        print(f"{targeted_audience}")
        else:
            print(f"{name} aucun bénéficiaire")
        return aid_targeted_audiences

    def extract_categories(self, line):
        """
        Exemple of string to process: [
                "Cimetière / Enclos paroissiaux",
                "Tiers-lieux",
                "Assainissement des eaux",
                "Mobilités",
                "Biodiversité",
                "Famille et enfance",
                "Pratiques artistiques et culturelles"
            ]
        """
        categories = line.get("categories", "")
        name = line["name"][:180]
        aid_categories = []
        if categories != [""]:
            for category in categories:
                if category in CATEGORIES_DICT:
                    aid_categories.extend(CATEGORIES_DICT.get(category, []))
                else:
                    self.stdout.write(
                        self.style.ERROR(f"Category '{category}' not mapped")
                    )
        else:
            print(f"no categories for aid '{name}'")
        return aid_categories

    def extract_keywords(self, line):
        categories = line.get("categories", [])
        keywords = []
        if categories != []:
            for category in categories:
                if category != []:
                    try:
                        keyword = Keyword.objects.get(name=category)
                        keyword_list = []
                        keyword_list.append(keyword)
                        keywords.extend(keyword_list)
                    except Exception:
                        try:
                            keyword = Keyword.objects.create(name=category)
                            keyword_list = []
                            keyword_list.append(keyword)
                            keywords.extend(keyword_list)
                        except Exception as e:
                            print(e)
        return keywords

    def extract_contact(self, line):
        if line.get("contact", None) is not None:
            contact = line.get("contact", "")
        else:
            contact = ""

        if line.get("contact_phone", ""):
            contact += line.get("contact_phone")
        return contact

    def extract_destinations(self, line):
        """
        Source format: list of strings
        These strings match our values from Aid.DESTINATIONS, so we just have
        to revert the dict to get the key
        """
        DESTINATIONS_DICT = {v: k for k, v in dict(Aid.DESTINATIONS).items()}
        aid_destinations = []

        destinations = line.get("destinations", [])

        if destinations:
            for destination in destinations:
                destination = destination.replace("'", "’")
                aid_destinations.append(DESTINATIONS_DICT[destination])

        return aid_destinations
