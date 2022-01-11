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


ADMIN_ID = 1

DATA_SOURCE = DataSource.objects \
    .prefetch_related('perimeter', 'backer') \
    .get(pk=6)

OPENDATA_URL = 'https://www.economie.gouv.fr/plan-de-relance/mesures/open-data'
FEED_ROWS = 1000

AUDIENCES_DICT = {}
AUDIENCES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/plan_france_relance_audiences_mapping.csv'
SOURCE_COLUMN_NAME = 'Bénéficiaires Plan France Relance'
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

CATEGORIES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/plan_france_relance_categories_mapping.csv'
SOURCE_COLUMN_NAME = 'Thématique Plan France Relance'
AT_COLUMN_NAMES = ['Sous-thématique AT 1', 'Sous-thématique AT 2', 'Sous-thématique AT 3']
CATEGORIES_DICT = mapping_categories(CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES)

SOURCE_COLUMN_NAME = 'Thématique Plan France Relance'
AT_COLUMN_NAMES = ['Thématique AT 1', 'Thématique AT 2', 'Thématique AT 3']
THEMATIQUES_DICT = mapping_categories(CATEGORIES_MAPPING_CSV_PATH, SOURCE_COLUMN_NAME, AT_COLUMN_NAMES)


class Command(BaseImportCommand):
    """
    Import data from the Plan France Relance Open Data plateform.
    """

    def add_arguments(self, parser):
        parser.add_argument('data-file', nargs='?', type=str)

    def handle(self, *args, **options):
        DATA_SOURCE.date_last_access = timezone.now()
        DATA_SOURCE.save()
        super().handle(*args, **options)

    def fetch_data(self, **options):
        if options['data-file']:
            data_file = os.path.abspath(options['data-file'])
            data = json.load(open(data_file))
            self.stdout.write('Total number of aids: {}'.format(len(data)))
            for line in data:
                yield line
        else:
            headers = {'accept': 'application/json', 'content-type': 'application/json'}
            req = requests.get(DATA_SOURCE.import_api_url)
            data = req.json()
            self.stdout.write('Total number of aids: {}'.format(len(data)))
            for line in data:
                yield line

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        unique_id = 'PFR_{}'.format(line['nid'])
        return unique_id

    def extract_import_data_url(self, line):
        return OPENDATA_URL

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_import_raw_object(self, line):
        return line

    def extract_name(self, line):
        title = line['title'][:180]
        return title

    def extract_name_initial(self, line):
        name_initial = line['title'][:180]
        return name_initial

    def extract_description(self, line):
        # desc_1 & desc_2 already have <p></p> tags
        desc_1 = content_prettify(line.get('field_chapo', ''))
        if 'Qui peut en bénéficier ?' in line.get('field_paragraphes', ''):
            desc_2 = str(line.get('field_paragraphes', '').partition('Qui peut en bénéficier ?')[0])
            desc_2 = content_prettify(desc_2)
        else:
            desc_2 = content_prettify(line.get('field_paragraphes', ''))
        description = desc_1 + desc_2
        return description

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_origin_url(self, line):
        origin_url = line.get('view_node', '')
        return origin_url

    def extract_application_url(self, line):
        application_url = line.get('view_node', '')
        return application_url

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process: "PDR-Administration" + "Communes, Départements"
        Split the string, loop on the values and match to our AUDIENCES
        """
        audiences_1 = line.get('field_thematique', '').split(', ')
        audiences_2 = line.get('field_categorie_taxo', '').split(', ')

        aid_audiences = []
        for audience in audiences_1:
            if audience in AUDIENCES_DICT:
                aid_audiences.extend(AUDIENCES_DICT.get(audience, []))
            else:
                self.stdout.write(self.style.ERROR(f'Audience {audience} not mapped'))

        if aid_audiences == []:
            for audience in audiences_2:
                if audience in AUDIENCES_DICT:
                    aid_audiences.extend(AUDIENCES_DICT.get(audience, []))
                else:
                    self.stdout.write(self.style.ERROR(f'Audience {audience} not mapped'))
        return aid_audiences

    def extract_categories(self, line):
        """
        Exemple of string to process: "Emploi et formation, Jeunes"
        Split the string, loop on the values and match to our Categories
        """
        categories = line.get('field_thematique', '').split(', ')
        title = line['title'][:180]
        aid_categories = []
        if categories != ['']:
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

    def extract_contact(self, line):
        if 'Liens utiles et contacts' in line.get('field_paragraphes', ''):
            contact = str(line.get('field_paragraphes', '').partition('Liens utiles et contacts')[2])
        elif 'Documents utiles' in line.get('field_paragraphes', ''):
            contact = str(line.get('field_paragraphes', '').partition('Documents utiles')[2])
        elif 'Liens utiles' in line.get('field_paragraphes', ''):
            contact = str(line.get('field_paragraphes', '').partition('Liens utiles')[2])
        else:
            contact = ''

        if 'Mise en ligne' in contact:
            contact = str(contact.partition('Mise en ligne')[0])
        elif 'Mis à jour' in contact:
            contact = str(contact.partition('Mis à jour')[0])

        contact_detail = content_prettify(contact)
        return contact_detail

    def extract_eligibility(self, line):
        if 'Qui peut en bénéficier ?' in line.get('field_paragraphes', ''):
            eligibility_part_1 = str(line.get('field_paragraphes', '').partition('Qui peut en bénéficier ?')[1])
            eligibility_part_2 = str(line.get('field_paragraphes', '').partition('Qui peut en bénéficier ?')[2])
            eligibility = eligibility_part_1 + eligibility_part_2 
        else:
            eligibility = ''

        if 'Liens utiles et contacts' in eligibility:
            eligibility = str(eligibility.partition('Liens utiles et contacts')[0])
        elif 'Documents utiles' in eligibility:
            eligibility = str(eligibility.partition('Documents utiles')[0])
        elif 'Liens utiles' in eligibility:
            eligibility = str(eligibility.partition('Liens utiles')[0])

        eligibility = content_prettify(eligibility)
        return eligibility
