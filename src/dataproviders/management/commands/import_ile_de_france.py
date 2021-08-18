# flake8: noqa
import os
import requests
from datetime import datetime

from django.utils import timezone

from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify, mapping_audiences, mapping_categories
from dataproviders.management.commands.base import BaseImportCommand
from aids.models import Aid


ADMIN_ID = 1

DATA_SOURCE = DataSource.objects \
    .prefetch_related('perimeter', 'backer') \
    .get(pk=4)

AUDIENCES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/ile_de_france_audiences_mapping.csv'
AUDIENCES_MAPPING_SOURCE_COLUMN_NAME = 'Bénéficiaires IDF'  # 'Code Bénéficiaires IDF'
AUDIENCES_MAPPING_AT_COLUMN_NAMES = ['Bénéficiaires AT 1']
AUDIENCES_DICT = mapping_audiences(AUDIENCES_MAPPING_CSV_PATH, AUDIENCES_MAPPING_SOURCE_COLUMN_NAME, AUDIENCES_MAPPING_AT_COLUMN_NAMES)

CATEGORIES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/ile_de_france_categories_mapping.csv'
CATEGORIES_MAPPING_SOURCE_COLUMN_NAME = 'Sous-thématiques IDF'  # 'Code Sous-thématiques IDF'
CATEGORIES_MAPPING_AT_COLUMN_NAMES = ['Sous-thématiques AT 1', 'Sous-thématiques AT 2']
CATEGORIES_DICT = mapping_categories(CATEGORIES_MAPPING_CSV_PATH, CATEGORIES_MAPPING_SOURCE_COLUMN_NAME, CATEGORIES_MAPPING_AT_COLUMN_NAMES)

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
DATE_FORMAT_ALTERNATIVE = '%Y-%m-%dT%H:%M:%SZ'


def try_parsing_date(date_raw):
    for date_format in (DATE_FORMAT, DATE_FORMAT_ALTERNATIVE):
        try:
            return datetime.strptime(date_raw, date_format)
        except ValueError:
            pass


class Command(BaseImportCommand):
    """
    Import data from the IDF (MGDIS) API.
    288 aids as of August 2021

    Usage:
    python manage.py import_ile_de_france
    """

    def handle(self, *args, **options):
        DATA_SOURCE.date_last_access = timezone.now()
        DATA_SOURCE.save()
        super().handle(*args, **options)

    def fetch_data(self, **options):
        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        req = requests.get(DATA_SOURCE.import_api_url, headers=headers)
        data = req.json()
        self.stdout.write('Total number of aids: {}'.format(len(data)))
        for line in data:
            yield line

    def line_should_be_processed(self, line):
        return True

    # Import-related stuff

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        return line['reference']

    def extract_import_data_url(self, line):
        return DATA_SOURCE.import_data_url

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_import_raw_object(self, line):
        return line

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    # Aid-related stuff

    def extract_name(self, line):
        return line['title'][:180]

    def extract_description(self, line):
        desc_1 = content_prettify(line.get('entete', ''))
        desc_2 = content_prettify(line.get('objectif', ''))
        desc_3 = content_prettify(line.get('modalite', ''))
        desc_4 = content_prettify(line.get('demarches', ''))
        desc_5 = content_prettify(line.get('notes', ''))
        description = desc_1 + desc_2 + desc_3 + desc_4 + desc_5
        return description

    def extract_targeted_audiences(self, line):
        """
        Source format: list of dicts
        Get the objects, loop on the values and match to our AUDIENCES
        """
        aid_audiences = []
        for audience in line.get('publicsBeneficiaire', []):
            audience_name = audience['title']
            if audience_name in AUDIENCES_DICT:
                aid_audiences.extend(AUDIENCES_DICT.get(audience_name, []))
            else:
                self.stdout.write(self.style.ERROR(f'Audience {audience_name} not mapped'))
                # self.stdout.write(self.style.ERROR(f'{audience_name}'))
        return aid_audiences

    def extract_categories(self, line):
        """
        Source format: list of dicts
        Get the objects, loop on the values and match to our Categories
        """
        aid_categories = []
        for category in line.get('competences', []):
            category_name = category['title']
            if category_name in CATEGORIES_DICT:
                aid_categories.extend(CATEGORIES_DICT.get(category_name, []))
            else:
                self.stdout.write(self.style.ERROR(f'Category {category_name} not mapped'))
                # self.stdout.write(self.style.ERROR(f'{category_name}'))
        return aid_categories

    # def extract_origin_url(self, line):
    #     return ?

    def extract_contact(self, line):
        return line.get('contact', '')

    # def extract_application_url(self, line):
    #     return line['teleservices']

    # def extract_aid_types(self, line):
    #     aid_type = line.get('kind', '')
    #     return [Aid.TYPES.grant]

    def extract_recurrence(self, line):
        next_date = line.get('dateDebutFuturCampagne', '')
        if next_date:
            return Aid.RECURRENCES.recurring
        return Aid.RECURRENCES.oneoff

    def extract_start_date(self, line):
        start_date_raw = line.get('dateOuvertureCampagne', '')
        if start_date_raw:
            start_date = try_parsing_date(start_date_raw)
            return start_date

    def extract_submission_deadline(self, line):
        end_date_raw = line.get('dateFinCampagne')
        if end_date_raw:
            end_date = try_parsing_date(end_date_raw)
            return end_date
