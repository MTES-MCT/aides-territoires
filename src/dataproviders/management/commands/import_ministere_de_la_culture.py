# flake8: noqa
import os
import csv
import json
import locale
import requests
import re
from datetime import datetime

from django.utils import timezone
from django.utils.text import slugify

from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify, mapping_categories
from dataproviders.management.commands.base import BaseImportCommand
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid
from categories.models import Theme, Category
from keywords.models import Keyword

ADMIN_ID = 1

DATA_SOURCE = DataSource.objects.prefetch_related("perimeter", "backer").get(pk=8)

OPENDATA_URL = "https://www.culture.gouv.fr/api/online-procedures"
FEED_ROWS = 1000

AUDIENCES_DICT = {}
AUDIENCES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/ministere_de_la_culture_audiences_mapping.csv"
)
SOURCE_COLUMN_NAME = "Bénéficiaires Ministère de la Culture"
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
                    audience = next(
                        choice[0]
                        for choice in Aid.AUDIENCES
                        if choice[1] == row[column]
                    )
                    AUDIENCES_DICT[row[SOURCE_COLUMN_NAME]].append(audience)

CATEGORIES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/ministere_de_la_culture_categories_mapping.csv"
)
SOURCE_COLUMN_NAME = "Thématique Ministère de la Culture"
AT_COLUMN_NAMES = [
    "Sous-thématique AT 1",
    "Sous-thématique AT 2",
    "Sous-thématique AT 3",
]
CATEGORIES_DICT = mapping_categories(
    CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES
)

SOURCE_COLUMN_NAME = "Thématique Ministère de la Culture"
AT_COLUMN_NAMES = ["Thématique AT 1", "Thématique AT 2", "Thématique AT 3"]
THEMATIQUES_DICT = mapping_categories(
    CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES
)


class Command(BaseImportCommand):
    """
    Import data from the Ministère de la Culture Open Data plateform.
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
            headers = {"accept": "application/json", "content-type": "application/json"}
            req = requests.get(DATA_SOURCE.import_api_url)
            data = json.loads(req.text)
            self.stdout.write("Total number of aids: {}".format(data["count"]))
            for line in data["results"]:
                yield line

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        unique_id = "MdC_{}".format(line["id"])
        return unique_id

    def extract_import_data_url(self, line):
        return OPENDATA_URL

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_import_raw_object_calendar(self, line):
        import_raw_object_calendar = {}
        import_raw_object_calendar["deadline"] = line["deadline"]
        return import_raw_object_calendar

    def extract_import_raw_object(self, line):
        import_raw_object = dict(line)
        import_raw_object.pop("deadline")
        return import_raw_object

    def extract_name(self, line):
        title = line["title"][:180]
        return title

    def extract_name_initial(self, line):
        name_initial = line["title"][:180]
        return name_initial

    def extract_description(self, line):
        desc_1 = content_prettify(line.get("summary", ""))
        desc_2 = content_prettify(line.get("body", ""))
        if line.get("type", "") == ["Demande d'autorisation"] or line.get(
            "type", ""
        ) == ["Demande de labellisation"]:
            aid_to_delete = "Aide à supprimer : type d'aides non correspondant"
            description = aid_to_delete + desc_1 + desc_2
            return description
        description = desc_1 + desc_2
        return description

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_origin_url(self, line):
        origin_url = line.get("url", "")
        return origin_url

    def extract_application_url(self, line):
        return ""

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process: "PDR-Administration" + "Communes, Départements"
        Split the string, loop on the values and match to our AUDIENCES
        """

        if line.get("public", ""):
            audiences = line.get("public", "").split(", ")

            aid_audiences = []
            for audience in audiences:
                if audience in AUDIENCES_DICT:
                    aid_audiences.extend(AUDIENCES_DICT.get(audience, []))
                else:
                    self.stdout.write(
                        self.style.ERROR(f"Audience {audience} not mapped")
                    )
            return aid_audiences
        else:
            pass

    def extract_categories(self, line):
        """
        Exemple of string to process: "Emploi et formation, Jeunes"
        Split the string, loop on the values and match to our Categories
        """
        categories = line.get("eztag_theme", [])
        title = line["title"][:180]
        aid_categories = []
        if categories != []:
            for category in categories:
                if category in CATEGORIES_DICT:
                    aid_categories.extend(CATEGORIES_DICT.get(category, []))
                elif category in THEMATIQUES_DICT:
                    aid_categories.extend(THEMATIQUES_DICT.get(category, []))
                else:
                    self.stdout.write(self.style.ERROR(f"{category}"))
        else:
            print(f"{title}")
        return aid_categories

    def extract_keywords(self, line):
        categories = line.get("eztag_theme", [])
        keywords = []
        if categories != []:
            for category in categories:
                try:
                    keyword = Keyword.objects.get(name=category)
                    keyword_list = []
                    keyword_list.append(keyword)
                    keyword_pk = Keyword.objects.get(name=category).pk
                    keywords.extend(keyword_list)
                except:
                    try:
                        keyword = Keyword.objects.create(name=category)
                        keyword_list = []
                        keyword_list.append(keyword)
                        keyword_pk = Keyword.objects.get(name=category).pk
                        keywords.extend(keyword_list)
                    except:
                        pass
        return keywords

    def extract_contact(self, line):
        contact = line.get("contact", "")
        contact = content_prettify(contact)
        return contact

    def extract_eligibility(self, line):
        eligibility = ""
        if line.get("amount") is not None:
            eligibility += line.get("amount", "")
        if line.get("public") is not None:
            eligibility += f"<br/> bénéficiaires de l'aide: {line.get('public')}"
        if line.get("eztag_region") is not None:
            eligibility += f"<br/> périmètre de l'aide: {line.get('eztag_region')}"
        if line.get("deadline"):
            if not line.get("deadline")[0].isdigit():
                eligibility += (
                    f"<br/> date de clôture de l'aide : {line.get('deadline')}"
                )
        eligibility = content_prettify(eligibility)
        return eligibility

    def extract_submission_deadline(self, line):
        if line.get("deadline"):
            if line.get("deadline")[0].isdigit():
                locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
                deadline = line.get("deadline")
                if "1er" in deadline:
                    deadline = re.sub("1er", "1", line.get("deadline"))
                submission_deadline = datetime.strptime(deadline, "%d %B %Y")
                return submission_deadline
        else:
            pass

    def extract_recurrence(self, line):
        if line.get("deadline"):
            recurrence = Aid.RECURRENCES.oneoff
        else:
            recurrence = Aid.RECURRENCES.ongoing
        return recurrence

    def extract_is_call_for_project(self, line):
        if line.get("deadline"):
            is_call_for_project = True
        else:
            is_call_for_project = False
        return is_call_for_project

    def extract_aid_types(self, line):
        if (
            line.get("type", "") == ["Subvention"]
            or line.get("type", "") == ["Aide"]
            or line.get("type", "") == ["Aide & subvention"]
        ):
            return [Aid.TYPES.grant]
        else:
            return []
