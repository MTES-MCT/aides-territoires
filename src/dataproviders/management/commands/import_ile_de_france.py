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
    .get(pk=4)

OPENDATA_URL = 'https://data.iledefrance.fr/api/records/1.0/search/?dataset=aides-appels-a-projets&q=&rows=1000'
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
        if options['data-file']:
            data_file = os.path.abspath(options['data-file'])
            data = json.load(open(data_file))
            for line in data['data']:
                yield line
        else:
            req = requests.get(DATA_SOURCE.import_api_url)
            req.encoding = 'utf-8-sig'  # We need this to take care of the bom
            data = json.loads(req.text)
            self.stdout.write('Total number of aids: {}'.format(data['nhits']))
            if data['nhits'] > FEED_ROWS:
                self.stdout.write(self.style.ERROR(
                    'Only fetching {} aids, but there are {} aids'.format(FEED_ROWS, data['nhits'])))
            self.stdout.write('Number of aids processing: {}'.format(len(data['records'])))
            for line in data['records']:
                yield line['fields']

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        unique_id = 'IDF_{}'.format(line['id'])
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
        if line.get('docinformatif01_nom', ''):
            desc += '<p><a href="' + line.get('docinformatif01_url', '') + '">' + line.get('docinformatif01_nom', '') + '</a></p>'
        if line.get('docinformatif02_nom', ''):
            desc += '<p><a href="' + line.get('docinformatif02_url', '') + '">' + line.get('docinformatif02_nom', '') + '</a></p>'
        if line.get('docinformatif03_nom', ''):
            desc += '<p><a href="' + line.get('docinformatif03_url', '') + '">' + line.get('docinformatif03_nom', '') + '</a></p>'
        if line.get('docinformatif04_nom', ''):
            desc += '<p><a href="' + line.get('docinformatif04_url', '') + '">' + line.get('docinformatif04_nom', '') + '</a></p>'
        return desc

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_origin_url(self, line):
        title = line.get('title', '')
        title_slugified = slugify(title)
        base_url = "https://www.iledefrance.fr/"
        origin_url = base_url + title_slugified
        return origin_url

    def extract_application_url(self, line):
        title = line.get('title', '')
        title_slugified = slugify(title)
        base_url = "https://www.iledefrance.fr/"
        application_url = base_url + title_slugified
        return application_url

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process: "Associations;Collectivités - Institutions;Entreprises"
        Split the string, loop on the values and match to our AUDIENCES
        """
        audiences = line.get('publics', '').split(';')
        aid_audiences = []
        for audience in audiences:
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
        categories = line.get('competences_', '').split(';')
        title = line['title'][:180]
        aid_categories = []
        if categories != ['']:
            for category in categories:
                if category in CATEGORIES_DICT:
                    aid_categories.extend(CATEGORIES_DICT.get(category, []))
                else:
                    self.stdout.write(self.style.ERROR(f"{category}"))
        else:
            print(f"{title}")
        return aid_categories

    def extract_contact(self, line):
        contact = line.get('contact', '')
        return contact

    def extract_eligibility(self, line):
        eligibility = line.get('publicsbeneficiaireprecision', '')
        eligibility += '<br>'
        eligibility += line.get('modalite', '')
        eligibility += '<br>'
        eligibility += line.get('objectif', '')
        eligibility += '<br>'
        eligibility += line.get('demarches', '')
        eligibility += '<br>'
        if line.get('docnecessaire01_nom', ''):
            eligibility += '<p><a href="' + line.get('docnecessaire01_url', '') + '">' + line.get('docnecessaire01_nom', '') + '</a></p>'
        if line.get('docnecessaire02_nom', ''):
            eligibility += '<p><a href="' + line.get('docnecessaire02_url', '') + '">' + line.get('docnecessaire02_nom', '') + '</a></p>'
        if line.get('docnecessaire03_nom', ''):
            eligibility += '<p><a href="' + line.get('docnecessaire03_url', '') + '">' + line.get('docnecessaire03_nom', '') + '</a></p>'
        if line.get('docnecessaire04_nom', ''):
            eligibility += '<p><a href="' + line.get('docnecessaire04_url', '') + '">' + line.get('docnecessaire04_nom', '') + '</a></p>'
        eligibility = content_prettify(eligibility)
        return eligibility
