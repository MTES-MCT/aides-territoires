# flake8: noqa
import os
import csv
import json
import html
import requests
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
from keywords.models import Keyword

ADMIN_ID = 1

DATA_SOURCE = DataSource.objects.prefetch_related("perimeter", "backer").get(pk=7)

OPENDATA_URL = "https://www.welcomeurope.com/"
FEED_ROWS = 1000

AUDIENCES_DICT = {}
AUDIENCES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/welcome_europe_audiences_mapping.csv"
)
SOURCE_COLUMN_NAME = "Bénéficiaires Welcome Europe"
AT_COLUMN_NAMES = [
    "Bénéficiaires AT 1",
    "Bénéficiaires AT 2",
    "Bénéficiaires AT 3",
    "Bénéficiaires AT 4",
    "Bénéficiaires AT 5",
    "Bénéficiaires AT 6",
    "Bénéficiaires AT 7",
    "Bénéficiaires AT 8",
    "Bénéficiaires AT 9",
    "Bénéficiaires AT 10",
    "Bénéficiaires AT 11",
    "Bénéficiaires AT 12",
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

TYPES_DICT = {}
TYPES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/welcome_europe_types_mapping.csv"
)
SOURCE_COLUMN_NAME = "Types Welcome Europe"
AT_COLUMN_NAMES = ["Types AT 1"]
with open(TYPES_MAPPING_CSV_PATH) as csv_file:
    csvreader = csv.DictReader(csv_file, delimiter=",")
    for index, row in enumerate(csvreader):
        if row[AT_COLUMN_NAMES[0]]:
            TYPES_DICT[row[SOURCE_COLUMN_NAME]] = []
            for column in AT_COLUMN_NAMES:
                if row[column]:
                    types = next(
                        choice[0] for choice in Aid.TYPES if choice[1] == row[column]
                    )
                    TYPES_DICT[row[SOURCE_COLUMN_NAME]].append(types)

CATEGORIES_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/welcome_europe_categories_mapping.csv"
)
SOURCE_COLUMN_NAME = "Thématique Welcome Europe"
AT_COLUMN_NAMES = ["Sous-Thématique AT 1", "Sous-Thématique AT 2"]
CATEGORIES_DICT = mapping_categories(
    CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES
)

PROGRAMS_MAPPING_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/../../data/welcome_europe_programs_mapping.csv"
)
SOURCE_COLUMN_NAME = "Programme Welcome Europe"
AT_COLUMN_NAMES = ["Programme AT 1"]
PROGRAMS_DICT = mapping_categories(
    PROGRAMS_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES
)


class Command(BaseImportCommand):
    """
    Import data from the Welcome Europe Data plateform.
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
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
            }
            req = requests.get(DATA_SOURCE.import_api_url, headers=headers)
            data = req.json()
            self.stdout.write("Total number of aids: {}".format(len(data)))
            for line in data:
                yield line

    def line_should_be_processed(self, line):
        return True

    def extract_keywords(self, line):
        categories = html.unescape(line.get("filtres_sectors", "")).split(";")
        keywords = []
        if categories != [""]:
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
                    except:
                        pass
        return keywords

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        unique_id = "WE_{}".format(line["ID"])
        return unique_id

    def extract_import_data_url(self, line):
        return ""

    def extract_import_data_mention(self, line):
        return "Cette aide est issue d'une traduction, réalisée par la société WelcomEurope à partir des données présentes sur le site officiel 'Funding & Tenders', elle a été mise a disposition d'Aides-territoires à titre gracieux."

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_import_raw_object_calendar(self, line):
        import_raw_object_calendar = {}
        if line.get("deadline1", None) != None:
            import_raw_object_calendar["deadline1"] = line["deadline1"]
        if line.get("dates_statut", None) != None:
            import_raw_object_calendar["dates_statut"] = line["dates_statut"]
        if line.get("dates_publication", None) != None:
            import_raw_object_calendar["dates_publication"] = line["dates_publication"]
        if line.get("dates_open-1", None) != None:
            import_raw_object_calendar["dates_open-1"] = line["dates_open-1"]
        if line.get("dates_open-2", None) != None:
            import_raw_object_calendar["dates_open-2"] = line["dates_open-2"]
        if line.get("dates_open-3", None) != None:
            import_raw_object_calendar["dates_open-3"] = line["dates_open-3"]
        if line.get("dates_open-4", None) != None:
            import_raw_object_calendar["dates_open-4"] = line["dates_open-4"]
        if line.get("dates_open-5", None) != None:
            import_raw_object_calendar["dates_open-5"] = line["dates_open-5"]
        if line.get("dates_deadline1", None) != None:
            import_raw_object_calendar["dates_deadline1"] = line["dates_deadline1"]
        if line.get("dates_deadline-2", None) != None:
            import_raw_object_calendar["dates_deadline-2"] = line["dates_deadline-2"]
        if line.get("dates_deadline-3", None) != None:
            import_raw_object_calendar["dates_deadline-3"] = line["dates_deadline-3"]
        if line.get("dates_deadline-4", None) != None:
            import_raw_object_calendar["dates_deadline-4"] = line["dates_deadline-4"]
        if line.get("dates", None) != None:
            import_raw_object_calendar["dates"] = line["dates"]
        return import_raw_object_calendar

    def extract_import_raw_object(self, line):
        import_raw_object = dict(line)
        if line.get("deadline1", None) != None:
            import_raw_object.pop("deadline1")
        if line.get("dates_statut", None) != None:
            import_raw_object.pop("dates_statut")
        if line.get("dates_publication", None) != None:
            import_raw_object.pop("dates_publication")
        if line.get("dates_open-1", None) != None:
            import_raw_object.pop("dates_open-1")
        if line.get("dates_open-2", None) != None:
            import_raw_object.pop("dates_open-2")
        if line.get("dates_open-3", None) != None:
            import_raw_object.pop("dates_open-3")
        if line.get("dates_open-4", None) != None:
            import_raw_object.pop("dates_open-4")
        if line.get("dates_open-5", None) != None:
            import_raw_object.pop("dates_open-5")
        if line.get("dates_deadline1", None) != None:
            import_raw_object.pop("dates_deadline1")
        if line.get("dates_deadline-2", None) != None:
            import_raw_object.pop("dates_deadline-2")
        if line.get("dates_deadline-3", None) != None:
            import_raw_object.pop("dates_deadline-3")
        if line.get("dates_deadline-4", None) != None:
            import_raw_object.pop("dates_deadline-4")
        if line.get("dates", None) != None:
            import_raw_object.pop("dates")
        return import_raw_object

    def extract_recurrence(self, line):
        if line.get("dates_deadline-2", None) or line.get("dates_open-2", None):
            recurrence = Aid.RECURRENCES.recurring
        else:
            recurrence = Aid.RECURRENCES.oneoff
        return recurrence

    def extract_european_aid(self, line):
        return Aid.EUROPEAN_AIDS.sectorial

    def extract_name(self, line):
        title = line["post_title"][:180]
        return title

    def extract_name_initial(self, line):
        name_initial = line["post_title"][:180]
        return name_initial

    def extract_short_title(self, line):
        short_title = line["info_references"][:64]
        return short_title

    def extract_description(self, line):
        programs_list = html.unescape(line.get("relations_programmes", "")).split(";")
        programs = "<p>" + "<br/>".join(programs_list) + "</p>"
        banner_chapeau = line.get("banner_chapeau", "")
        banner_budget = line.get("banner_budget", "")
        info_amount = line.get("info_amount", "")
        info_amorce = line.get("info_amorce", "")
        info_priories = line.get("info_priories", "")

        description = (
            "<div>"
            + programs
            + "<p>-----</p>"
            + banner_chapeau
            + "<p>-----</p>"
            + banner_budget
            + "<p>-----</p>"
            + info_amount
            + "<p>-----</p>"
            + info_amorce
            + "<p>-----</p>"
            + info_priories
            + "</div>"
        )
        return description

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_eligibility(self, line):
        eligibility = content_prettify(line.get("info_info-regions", ""))
        return eligibility

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_origin_url(self, line):
        return ""

    def extract_application_url(self, line):
        return ""

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process: "Centres de recherche,Autorités locales et régionales,Grandes entreprises,ONG de Développement,PME,Universités,Organisations Internationales,ONG,Association & ONG,Collectivité Territoriale & Entité Affiliée,Centre de recherche & université,Grande Entreprise (> 250 Salaries),Organisation UE & Internationale,Pme & Start-Up (< 249 Salaries)"
        Split the string, loop on the values and match to our AUDIENCES
        """
        audiences = line.get("filtres_beneficiaries", "").split(";")
        aid_audiences = []
        for audience in audiences:
            if audience in AUDIENCES_DICT:
                aid_audiences.extend(AUDIENCES_DICT.get(audience, []))
            else:
                self.stdout.write(self.style.ERROR(f"Audience {audience} not mapped"))
        return aid_audiences

    def extract_aid_types(self, line):
        """
        Exemple of string to process: "Appel à propositions"
        """
        types = line.get("info_categorie", "").split(",")
        aid_types = []
        for type_item in types:
            if type_item in TYPES_DICT:
                aid_types.extend(TYPES_DICT.get(type_item, []))
            else:
                self.stdout.write(self.style.ERROR(f"Type {type_item} not mapped"))
        return aid_types

    def extract_is_call_for_project(self, line):
        is_call_for_project = True
        return is_call_for_project

    def extract_start_date(self, line):
        if line.get("dates_open-5", None):
            start_date = datetime.strptime(line["dates_open-5"], "%Y%m%d")
            return start_date
        elif line.get("dates_open-4", None):
            start_date = datetime.strptime(line["dates_open-4"], "%Y%m%d")
            return start_date
        elif line.get("dates_open-3", None):
            start_date = datetime.strptime(line["dates_open-3"], "%Y%m%d")
            return start_date
        elif line.get("dates_open-2", None):
            start_date = datetime.strptime(line["dates_open-2"], "%Y%m%d")
            return start_date
        elif line.get("dates_open-1", None):
            start_date = datetime.strptime(line["dates_open-1"], "%Y%m%d")
            return start_date

    def extract_submission_deadline(self, line):
        if line.get("dates_deadline-4", None):
            submission_deadline = datetime.strptime(
                line["dates_deadline-4"], "%Y%m%d"
            ).date()
            return submission_deadline
        elif line.get("dates_deadline-3", None):
            submission_deadline = datetime.strptime(
                line["dates_deadline-3"], "%Y%m%d"
            ).date()
            return submission_deadline
        elif line.get("dates_deadline-2", None):
            submission_deadline = datetime.strptime(
                line["dates_deadline-2"], "%Y%m%d"
            ).date()
            return submission_deadline
        elif line.get("dates_deadline1", None):
            submission_deadline = datetime.strptime(
                line["dates_deadline1"], "%Y%m%d"
            ).date()
            return submission_deadline
        elif line.get("deadline1", None):
            submission_deadline = datetime.strptime(line["deadline1"], "%Y%m%d").date()
            return submission_deadline

    def extract_categories(self, line):
        """
        Exemple of string to process: "je decouvre les metiers;je choisis mon metier ou ma formation;je rebondis tout au long de la vie;je m'informe sur les metiers"  # noqa
        Split the string, loop on the values and match to our Categories
        """
        categories = html.unescape(line.get("filtres_sectors", "")).split(";")
        title = line["post_title"][:180]
        aid_categories = []
        if categories != [""]:
            for category in categories:
                if category in CATEGORIES_DICT:
                    aid_categories.extend(CATEGORIES_DICT.get(category, []))
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f"\"{line.get('filtres_sectors', '')}\";{category}"
                        )
                    )
        else:
            print(f"{title} aucune thématique WE")
        return aid_categories

    def extract_programs(self, line):
        """
        Exemple of string to process: "JPI - (1.) INITIATIVE DE PROGRAMMATION CONJOINTE;JPI - (1.11.) INITIATIVE DE PROGRAMMATION CONJOINTE PARTENARIAT POUR LA RECHERCHE ET L&rsquo;INNOVATION DANS LA REGION MEDITERRANEENNE (JPI PRIMA)"  # noqa
        Split the string, loop on the values and match to our Programs
        """
        programs = html.unescape(line.get("relations_programmes", "")).split(";")
        title = line["post_title"][:180]
        aid_programs = []
        if programs != [""]:
            for program in programs:
                if program in PROGRAMS_DICT:
                    aid_programs.extend(PROGRAMS_DICT.get(program, []))
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f"\"{line.get('relations_programmes', '')}\";{program}"
                        )
                    )
        else:
            print(f"{title} aucun programme WE")
        return aid_programs

    def extract_contact(self, line):
        info_utile_list = line.get("info_utile", "").split("  ")
        info_utile = "<p>" + "<br/>".join(info_utile_list) + "<p>"
        info_contact_list = line.get("info_contact", "").split("  ")
        info_contact = "<p>" + "<br/>".join(info_contact_list) + "<p>"
        info_advice_list = line.get("info_advice", "").split("  ")
        info_advice = "<p>" + "<br/>".join(info_advice_list) + "<p>"
        contact = (
            "<div>"
            + "<p> ----- </p>"
            + info_advice
            + "<p> ----- </p>"
            + info_contact
            + "<p> ----- </p>"
            + info_utile
            + "</div>"
        )
        return contact
