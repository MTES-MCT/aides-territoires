# flake8: noqa
import os
import csv
import json
import requests

from django.conf import settings
from django.utils import timezone

from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify
from dataproviders.management.commands.base import BaseImportCommand
from aids.models import Aid


DATA_SOURCE = DataSource.objects \
    .prefetch_related('perimeter', 'backer') \
    .get(pk=3)

OPENDATA_URL = ''

AUDIENCES_DICT = {}
AUDIENCES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/grand_est_audiences_mapping.csv'
SOURCE_COLUMN_NAME = 'Bénéficiaires Grand Est'
AT_COLUMN_NAMES = ['Bénéficiaires AT 1', 'Bénéficiaires AT 2', 'Bénéficiaires AT 3', 'Bénéficiaires AT 4']
with open(AUDIENCES_MAPPING_CSV_PATH) as csv_file:
    csvreader = csv.DictReader(csv_file, delimiter=",")
    for index, row in enumerate(csvreader):
        if row[AT_COLUMN_NAMES[0]]:
            AUDIENCES_DICT[row[SOURCE_COLUMN_NAME]] = []
            for column in AT_COLUMN_NAMES:
                if row[column]:
                    try:
                        audience = next(choice[0] for choice in Aid.AUDIENCES if choice[1] == row[column])
                        AUDIENCES_DICT[row[SOURCE_COLUMN_NAME]].append(audience)
                    except:
                        print(row[column])


class Command(BaseImportCommand):
    """
    Import data from the Grand Est API.
    219 aids as of May 2021

    Usage:
    python manage.py import_grand_est_api
    python manage.py import_grand_est_api grand-est.json
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
            req = requests.get(DATA_SOURCE.import_api_url, headers=headers, auth=(settings.GRAND_EST_API_USERNAME, settings.GRAND_EST_API_PASSWORD))
            data = req.json()
            self.stdout.write('Total number of aids: {}'.format(len(data)))
            for line in data:
                yield line

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        return line['ID']

    def extract_import_data_url(self, line):
        return DATA_SOURCE.import_data_url

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_name(self, line):
        return line['post_title'][:180]

    def extract_description(self, line):
        desc_1 = content_prettify(line.get('gui_introduction', ''))
        desc_2 = content_prettify(line.get('post_content', ''))
        description = desc_1 + desc_2
        return description

    def extract_targeted_audiences(self, line):
        """
        Source format: list of dicts
        Split the string, loop on the values and match to our AUDIENCES
        """
        audiences = line.get('aid_benef', [])
        aid_audiences = []
        for audience in audiences:
            if audience['name'] in AUDIENCES_DICT:
                aid_audiences.extend(AUDIENCES_DICT.get(audience, []))
            else:
                self.stdout.write(self.style.ERROR(f'Audience {audience} not mapped'))
        return aid_audiences

    def extract_origin_url(self, line):
        return line['url']

    def extract_contact(self, line):
        return line.get('gui_texte_gris', '')

    def extract_application_url(self, line):
        return line['gui_dematerialise_url']
