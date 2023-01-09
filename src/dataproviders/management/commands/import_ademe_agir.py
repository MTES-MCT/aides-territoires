import os
import csv
import requests
from datetime import datetime

from django.conf import settings
from django.utils import timezone

from aids.models import Aid
from keywords.models import Keyword
from geofr.models import Perimeter
from geofr.utils import attach_perimeters_check, combine_perimeters
from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import (
    content_prettify,
    mapping_categories,
    mapping_categories_label,
)
from dataproviders.management.commands.base import BaseImportCommand

ADMIN_ID = 1

DATA_SOURCE = DataSource.objects.prefetch_related("backer").get(pk=10)

AUDIENCES_DICT = {}
AUDIENCES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/ademe_agir_audiences_mapping.csv"
)
SOURCE_COLUMN_NAME = "Code Bénéficiaires Ademe Agir"
AT_COLUMN_NAMES = [
    "Bénéficiaires AT 1",
    "Bénéficiaires AT 2",
    "Bénéficiaires AT 3",
    "Bénéficiaires AT 4",
    "Bénéficiaires AT 5",
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
                    except Exception:
                        print(row[column])

CATEGORIES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/ademe_agir_categories_mapping.csv"
)
SOURCE_COLUMN_NAME = "Réf Sous-thématique Ademe Agir"
SOURCE_COLUMN_LABEL = "Sous-thématique Ademe Agir"
AT_COLUMN_NAMES = [
    "Sous-thématique AT 1",
    "Sous-thématique AT 2",
    "Sous-thématique AT 3",
]
CATEGORIES_DICT = mapping_categories(
    CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES
)
CATEGORIES_LABEL_DICT = mapping_categories_label(
    CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, SOURCE_COLUMN_LABEL
)

SOURCE_COLUMN_NAME = "Réf Thématique Ademe Agir"
AT_COLUMN_NAMES = [
    "Sous-thématique AT 1",
    "Sous-thématique AT 2",
    "Sous-thématique AT 3",
]
THEMATIQUES_DICT = mapping_categories(
    CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES
)


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

    def extract_import_data_mention(self, line):
        return "Ces données sont mises à disposition par l'ADEME."

    def extract_import_uniqueid(self, line):
        unique_id = "AGIR_{}".format(line["id"])
        return unique_id

    def extract_import_data_url(self, line):
        return DATA_SOURCE.import_data_url

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_import_raw_object_calendar(self, line):
        import_raw_object_calendar = {}
        if line.get("date_debut", None) is not None:
            import_raw_object_calendar["date_debut"] = line["date_debut"]
        if line.get("date_fin", None) is not None:
            import_raw_object_calendar["date_fin"] = line["date_fin"]
        return import_raw_object_calendar

    def extract_import_raw_object(self, line):
        import_raw_object = dict(line)
        if line.get("date_debut", None) is not None:
            import_raw_object.pop("date_debut")
        if line.get("date_fin", None) is not None:
            import_raw_object.pop("date_fin")
        return import_raw_object

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
        if line["url_agir"]:
            return line["url_agir"]
        else:
            return ""

    def extract_application_url(self, line):
        if line["url_agir"]:
            return line["url_agir"]
        else:
            return ""

    def extract_is_call_for_project(self, line):
        if line.get("type") == "AAP":
            return True
        else:
            return False

    def extract_aid_types(self, line):
        return [Aid.TYPES.grant, Aid.TYPES.technical_engineering]

    def extract_start_date(self, line):
        start_date = datetime.strptime(line.get("date_debut"), "%Y-%m-%dT%H:%M:%S%z")
        return start_date

    def extract_submission_deadline(self, line):
        submission_deadline = datetime.strptime(
            line.get("date_fin"), "%Y-%m-%dT%H:%M:%S%z"
        )
        return submission_deadline

    def extract_recurrence(self, line):
        if line.get("date_debut") and line.get("date_fin"):
            return Aid.RECURRENCES.oneoff
        else:
            return Aid.RECURRENCES.ongoing

    def extract_mobilization_steps(self, line):
        return [Aid.STEPS.op, Aid.STEPS.preop, Aid.STEPS.postop]

    def extract_perimeter(self, line):
        couv_geo = line.get("couverture_geo", [])["code"]
        if couv_geo == "1":
            return Perimeter.objects.get(code="FRA")
        elif couv_geo == "2" or couv_geo == "3":
            return Perimeter.objects.get(code="EU")
        elif couv_geo == "4":
            regions_code = line.get("regions", [])
            if len(regions_code) == 1:
                return Perimeter.objects.get(
                    code=regions_code[0], scale=Perimeter.SCALES.region
                )
            elif len(regions_code) > 1:
                regions_code_sorted = sorted(regions_code)
                regions_code_sorted_str = "_".join(regions_code_sorted)
                regions_code_str = f"regions_{regions_code_sorted_str}"
                try:
                    perimeter = Perimeter.objects.get(
                        name=regions_code_str, scale=Perimeter.SCALES.adhoc
                    )
                    print(f"Perimeter found: {perimeter}")
                    return perimeter
                except Exception:
                    try:
                        new_id = Perimeter.objects.last().pk + 1
                        perimeter = Perimeter.objects.create(
                            name=regions_code_str,
                            code=f"id_{new_id}",
                            scale=Perimeter.SCALES.adhoc,
                            is_visible_to_users=False,
                        )
                        print(f"Perimeter created: {perimeter}")
                        add_perimeters = []
                        for region in regions_code_sorted:
                            try:
                                region_object = Perimeter.objects.get(
                                    code=region, scale=Perimeter.SCALES.region
                                )
                            except Exception:
                                try:
                                    region_object = Perimeter.objects.get(
                                        code=region, scale=Perimeter.SCALES.adhoc
                                    )
                                except Exception:
                                    print(f"This region_code does not exist {region}")
                            add_perimeters.append(region_object)
                        rm_perimeters = []
                        city_codes = list(
                            combine_perimeters(add_perimeters, rm_perimeters)
                        )
                        attach_perimeters_check(
                            perimeter, city_codes, DATA_SOURCE.aid_author
                        )
                        return perimeter
                    except Exception as e:
                        print(e)
                        print(regions_code_str)

    def extract_eligibility(self, line):
        eligibility = ""
        couv_geo = line.get("couverture_geo", [])
        if couv_geo["code"] == "4":
            region_codes = line.get("regions", [])
            if len(region_codes) > 1:
                perimeters = []
                for region_code in region_codes:
                    try:
                        perimeters.append(
                            Perimeter.objects.get(
                                code=region_code, scale=Perimeter.SCALES.region
                            ).name
                        )
                    except Exception:
                        try:
                            perimeters.append(
                                Perimeter.objects.get(code=region_code).name
                            )
                        except Exception:
                            print(f"Code région : {region_code}")
                perimeters_str = ", ".join(perimeters)
                eligibility = f"Ce dispositif est applicable uniquement aux régions \
                    suivantes : {perimeters_str}"
                return eligibility
        return eligibility

    def extract_targeted_audiences(self, line):
        """
        Source format: list of dicts
        Get the objects, loop on the values and match to our AUDIENCES
        """
        audiences = line.get("cible_projet", [])
        aid_audiences = []
        for audience in audiences:
            if audience in AUDIENCES_DICT:
                aid_audiences.extend(AUDIENCES_DICT.get(audience, []))
            else:
                self.stdout.write(self.style.ERROR(f"Audience {audience} not mapped"))
        return aid_audiences

    def extract_categories(self, line):
        """
        Exemple of string to process: ['ENR', 'BOIBIO']
        Split the string, loop on the values and match to our Categories
        """
        categories = line.get("thematiques", [])
        title = line["titre"][:180]
        aid_categories = []
        if categories != [""]:
            for category in categories:
                if category in CATEGORIES_DICT:
                    aid_categories.extend(CATEGORIES_DICT.get(category, []))
                elif category in THEMATIQUES_DICT:
                    aid_categories.extend(THEMATIQUES_DICT.get(category, []))
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f"\"{line.get('thematiques', [])}\";{category}"
                        )
                    )
        else:
            print(f"{title} - {categories}")
        return aid_categories

    def extract_keywords(self, line):
        categories = line.get("thematiques", [])
        keywords = []
        if categories != []:
            for category in categories:
                category = CATEGORIES_LABEL_DICT.get(category, [])
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
        contact = """Pour contacter l’Ademe ou candidater à l'offre, veuillez cliquer
         sur le lien vers le descriptif complet."""
        return contact
