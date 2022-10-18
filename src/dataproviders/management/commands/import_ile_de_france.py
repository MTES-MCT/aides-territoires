# flake8: noqa
import os
import csv
import json
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
from categories.models import Theme, Category
from keywords.models import Keyword

ADMIN_ID = 1

DATA_SOURCE = DataSource.objects \
    .prefetch_related('perimeter', 'backer') \
    .get(pk=4)

OPENDATA_URL = 'https://mesdemarches.iledefrance.fr/guide-des-aides/api/public/tenants/cridfprd/aides?top=2500'
FEED_ROWS = 1000

AUDIENCES_DICT = {}
AUDIENCES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/ile_de_france_audiences_mapping.csv'
SOURCE_COLUMN_NAME = "Bénéficiaires Île-de-France"
AT_COLUMN_NAMES = ['Bénéficiaires AT 1', 'Bénéficiaires AT 2', 'Bénéficiaires AT 3', 'Bénéficiaires AT 4', 'Bénéficiaires AT 5']
with open(AUDIENCES_MAPPING_CSV_PATH) as csv_file:
    csvreader = csv.DictReader(csv_file, delimiter=",")
    for index, row in enumerate(csvreader):
        if row[AT_COLUMN_NAMES[0]]:
            AUDIENCES_DICT[row[SOURCE_COLUMN_NAME]] = []
            for column in AT_COLUMN_NAMES:
                if row[column]:
                    audience = next(choice[0] for choice in Aid.AUDIENCES if choice[1] == row[column])
                    AUDIENCES_DICT[row[SOURCE_COLUMN_NAME]].append(audience)

CATEGORIES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/ile_de_france_categories_mapping.csv'
SOURCE_COLUMN_NAME = "Thématique d'Île-de-France"
AT_COLUMN_NAMES = ['Sous-thématique AT 1']
CATEGORIES_DICT = mapping_categories(CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES)

SOURCE_COLUMN_NAME = "Thématique d'Île-de-France"
AT_COLUMN_NAMES = ['Thématique AT 1']
THEMATIQUES_DICT = mapping_categories(CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES)


class Command(BaseImportCommand):
    """
    Import data from the Conseil Régional d'Île-de-France Open Data plateform.
    """

    def add_arguments(self, parser):
        parser.add_argument('data-file', nargs='?', type=str)

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

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_data_mention(self, line):
        return "Ces données sont mises à disposition par le Conseil Régional d'Île-de-France."

    def extract_import_uniqueid(self, line):
        unique_id = 'IDF_{}'.format(line['reference'])
        return unique_id

    def extract_import_data_url(self, line):
        return OPENDATA_URL

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_import_raw_object_calendar(self, line):
        import_raw_object_calendar = {}
        if line.get("dateFinCampagne", None) != None:
            import_raw_object_calendar["dateFinCampagne"] = line["dateFinCampagne"]
        if line.get("dateOuvertureCampagne", None) != None:
            import_raw_object_calendar["dateOuvertureCampagne"] = line["dateOuvertureCampagne"]
        if line.get("dateDebutFuturCampagne", None) != None:
            import_raw_object_calendar["dateDebutFuturCampagne"] = line["dateDebutFuturCampagne"]
        if line.get("datePublicationSouhaitee", None) != None:
            import_raw_object_calendar["datePublicationSouhaitee"] = line["datePublicationSouhaitee"]
        return import_raw_object_calendar

    def extract_import_raw_object(self, line):
        import_raw_object = dict(line)
        if line.get("dateFinCampagne", None) != None:
            import_raw_object.pop("dateFinCampagne")
        if line.get("dateOuvertureCampagne", None) != None:
            import_raw_object.pop("dateOuvertureCampagne")
        if line.get("dateDebutFuturCampagne", None) != None:
            import_raw_object.pop("dateDebutFuturCampagne")
        if line.get("datePublicationSouhaitee", None) != None:
            import_raw_object.pop("datePublicationSouhaitee")
        return import_raw_object

    def extract_name(self, line):
        name = line['title'][:180]
        return name

    def extract_name_initial(self, line):
        name_initial = line['title'][:180]
        return name_initial

    def extract_description(self, line):
        desc = line.get('engagements', '')
        desc += '<br>'
        desc += line.get('entete', '')
        desc += '<br>'
        desc += line.get('notes', '')
        desc += '<br>'
        return desc

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_origin_url(self, line):
        title = line.get('reference', '')
        base_url = "https://www.iledefrance.fr/aides-appels-a-projets/"
        origin_url = base_url + title
        return origin_url

    def extract_application_url(self, line):
        title = line.get('reference', '')
        base_url = "https://www.iledefrance.fr/aides-appels-a-projets/"
        application_url = base_url + title
        return application_url

    def extract_mobilization_steps(self, line):
        return [Aid.STEPS.op, Aid.STEPS.preop, Aid.STEPS.postop]

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process: "Associations;Collectivités - Institutions;Entreprises"
        Split the string, loop on the values and match to our AUDIENCES
        """
        audiences = line.get('publicsBeneficiaire', '')
        aid_audiences = []
        for audience in audiences:
            if audience["title"] in AUDIENCES_DICT:
                aid_audiences.extend(AUDIENCES_DICT.get(audience["title"], []))
            else:
                audience_title = audience["title"]
                self.stdout.write(self.style.ERROR(f"Audience '{audience_title}' not mapped"))
        return aid_audiences

    def extract_categories(self, line):
        """
        Exemple of string to process: "Emploi et formation, Jeunes"
        Split the string, loop on the values and match to our Categories
        """
        categories = line.get('competences', '')
        title = line['title'][:180]
        aid_categories = []
        if categories != ['']:
            for category in categories:
                if category["title"] in CATEGORIES_DICT:
                    aid_categories.extend(CATEGORIES_DICT.get(category["title"], []))
                else:
                    category_title = category["title"]
                    self.stdout.write(self.style.ERROR(f"Category '{category_title}' not mapped"))
        else:
            print(f"no categories for aid '{title}'")
        return aid_categories

    def extract_contact(self, line):
        contact = line.get('contact', '')
        return contact

    def extract_eligibility(self, line):
        eligibility = line.get('publicsBeneficiairePrecision', '')
        eligibility += '<br>'
        eligibility += line.get('modalite', '')
        eligibility += '<br>'
        eligibility += line.get('objectif', '')
        eligibility += '<br>'
        eligibility += line.get('demarches', '')
        eligibility += '<br>'
        if line.get('documentsPublics', ''):
            eligibility += '<p><a href="' + line.get('docnecessaire01_url', '') + '">' + line.get('docnecessaire01_nom', '') + '</a></p>'
        if line.get('docnecessaire02_nom', ''):
            eligibility += '<p><a href="' + line.get('docnecessaire02_url', '') + '">' + line.get('docnecessaire02_nom', '') + '</a></p>'
        if line.get('docnecessaire03_nom', ''):
            eligibility += '<p><a href="' + line.get('docnecessaire03_url', '') + '">' + line.get('docnecessaire03_nom', '') + '</a></p>'
        if line.get('docnecessaire04_nom', ''):
            eligibility += '<p><a href="' + line.get('docnecessaire04_url', '') + '">' + line.get('docnecessaire04_nom', '') + '</a></p>'
        eligibility = content_prettify(eligibility)
        return eligibility

    def extract_recurrence(self, line):
        if line.get("dateDebutFuturCampagne", None):
            recurrence = Aid.RECURRENCES.recurring
        elif line.get("dateFinCampagne", None) :
            recurrence = Aid.RECURRENCES.oneoff
        else:
            recurrence = Aid.RECURRENCES.ongoing
        return recurrence

    def extract_start_date(self, line):
        # Some aids have a field "dateOuvertureCampagne" when other just don't
        # Moreover the format of "dateOuvertureCampagne" field is not unique
        # Date format can be '%Y-%m-%dT%H:%M:%S.%fZ' and sometimes '%Y-%m-%dT%H:%M:%SZ'
        if line.get("dateOuvertureCampagne", None):
            try:
                start_date = datetime.strptime(line["dateOuvertureCampagne"], '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                start_date = datetime.strptime(line["dateOuvertureCampagne"], '%Y-%m-%dT%H:%M:%SZ')
            return start_date

    def extract_submission_deadline(self, line):
        # Some aids have a field "dateFinCampagne" when other just don't
        # Moreover the format of "dateFinCampagne" field is not unique
        # Date format can be '%Y-%m-%dT%H:%M:%S.%fZ' and sometimes '%Y-%m-%dT%H:%M:%SZ'
        if line.get("dateFinCampagne", None):
            try:
                submission_deadline = datetime.strptime(line["dateFinCampagne"], '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                submission_deadline = datetime.strptime(line["dateFinCampagne"], '%Y-%m-%dT%H:%M:%SZ')
            return submission_deadline

    def extract_aid_types(self, line):
        return [Aid.TYPES.grant]

    def extract_keywords(self, line):
        categories = line.get('competences', '')
        keywords = []
        if categories != [""]:
            for category in categories:
                try:
                    keyword = Keyword.objects.get(name=category["title"])
                    keyword_list = []
                    keyword_list.append(keyword)
                    keywords.extend(keyword_list)
                except:
                    try:
                        keyword = Keyword.objects.create(name=category["title"])
                        keyword_list = []
                        keyword_list.append(keyword)
                    except:
                        pass
        return keywords
