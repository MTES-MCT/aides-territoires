import json
import os
import requests

from django.utils import timezone

from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import (
    content_prettify,
    mapping_categories,
)
from dataproviders.management.commands.base import BaseImportCommand


DATA_SOURCE = DataSource.objects.prefetch_related("backer").get(pk=11)

CATEGORIES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/occitanie_categories_mapping.csv"
)
SOURCE_COLUMN_NAME = "Thématique Occitanie"
AT_COLUMN_NAMES = [
    "Thématique AT 1",
    "Thématique AT 2",
    "Thématique AT 3",
]
CATEGORIES_DICT = mapping_categories(
    CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES
)


class Command(BaseImportCommand):
    """
    Import data from the Occitanie API.

    Usage:
    python manage.py import_occitanie
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
            self.stdout.write("Total number of aids: {}".format(len(data["records"])))
            for line in data["records"]:
                yield line
        else:
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
            }
            req = requests.get(DATA_SOURCE.import_api_url, headers=headers)
            data = req.json()
            self.stdout.write("Total number of aids: {}".format(len(data["records"])))
            for line in data["records"]:
                yield line

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_data_mention(self, line):
        return "Ces données sont mises à disposition par la Région Occitanie."

    def extract_import_uniqueid(self, line):
        unique_id = "OCCITANIE__{}".format(line["recordid"])
        return unique_id

    def extract_import_data_url(self, line):
        return DATA_SOURCE.import_data_url

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_import_raw_object_calendar(self, line):
        import_raw_object_calendar = {}
        return import_raw_object_calendar

    def extract_import_raw_object(self, line):
        import_raw_object = dict(line)
        return import_raw_object

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_name(self, line):
        title = line["fields"]["titre"]
        str_to_find = '<span class="titre_surligne">Appels à projets</span>'
        str_to_find_span_1 = '<span class="titre_surligne">'
        str_to_find_span_2 = "</span>"
        if str_to_find in title:
            title = str(title.partition(str_to_find)[2])
        elif str_to_find_span_1 in title:
            title = title.replace(str_to_find_span_1, "")
            title = title.replace(str_to_find_span_2, "")
        title = title[:180]
        return title

    def extract_name_initial(self, line):
        title = line["fields"]["titre"]
        str_to_find = '<span class="titre_surligne">Appels à projets</span>'
        str_to_find_span_1 = '<span class="titre_surligne">'
        str_to_find_span_2 = "</span>"
        if str_to_find in title:
            title = str(title.partition(str_to_find)[2])
        elif str_to_find_span_1 in title:
            title = title.replace(str_to_find_span_1, "")
            title = title.replace(str_to_find_span_2, "")
        title = title[:180]
        return title

    def extract_description(self, line):
        description = ""
        description += content_prettify(line["fields"].get("chapo", ""))
        description += content_prettify(line["fields"].get("introduction", ""))
        return description

    def extract_origin_url(self, line):
        return line["fields"]["url"]

    def extract_is_call_for_project(self, line):
        if line["fields"].get("type", "") == "Appels à projets":
            return True
        else:
            return False

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_categories(self, line):
        """
        Exemple of string to process: "Culture, Environnement - Climat, Citoyenneté et démocratie"
        Split the string, loop on the values and match to our Categories
        """
        categories = line["fields"].get("thematiques", "").split(",")
        title = line["fields"]["titre"][:180]
        aid_categories = []
        if categories != [""]:
            for category in categories:
                if category in CATEGORIES_DICT:
                    aid_categories.extend(CATEGORIES_DICT.get(category, []))
                else:
                    print(f"{title} - {category}")
        else:
            print(f"{title} - {categories}")
        return aid_categories

    def extract_contact(self, line):
        contact = """Pour contacter la Région Occitanie ou candidater à l'offre, veuillez cliquer
         sur le bouton 'Plus d'informations' ou sur le bouton 'Candidater à l'aide'."""
        return contact
