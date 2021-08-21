# flake8: noqa
import os
import csv
import json
import requests
from datetime import datetime

from django.conf import settings
from django.utils import timezone

from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import (
    content_prettify, extract_mapping_values_from_list,
    build_audiences_mapping_dict, build_categories_mapping_dict)
from dataproviders.management.commands.base import BaseImportCommand
from aids.models import Aid


ADMIN_ID = 1

DATA_SOURCE = DataSource.objects \
    .prefetch_related('perimeter', 'backer') \
    .get(pk=3)

AUDIENCES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/grand_est_api_audiences_mapping.csv'
AUDIENCES_DICT = build_audiences_mapping_dict(
    AUDIENCES_MAPPING_CSV_PATH,
    source_column_name='Bénéficiaires Grand Est',
    at_column_names=['Bénéficiaires AT 1', 'Bénéficiaires AT 2', 'Bénéficiaires AT 3', 'Bénéficiaires AT 4'])

CATEGORIES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/grand_est_api_categories_mapping.csv'
CATEGORIES_DICT = build_categories_mapping_dict(
    CATEGORIES_MAPPING_CSV_PATH,
    source_column_name='Sous-thématiques Grand Est',  # 'Thématiques Grand Est'
    at_column_names=['Sous-thématiques AT 1', 'Sous-thématiques AT 2', 'Sous-thématiques AT 3', 'Sous-thématiques AT 4', 'Sous-thématiques AT 5', 'Sous-thématiques AT 6', 'Sous-thématiques AT 7', 'Sous-thématiques AT 8'])


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

    def extract_import_raw_object(self, line):
        return line

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_name(self, line):
        return line['post_title'][:180]

    def extract_description(self, line):
        # desc_1 = content_prettify(line.get('gui_introduction', ''))
        description = content_prettify(line.get('post_content', ''))
        # description = desc_1 + desc_2
        return description

    def extract_targeted_audiences(self, line):
        source_audiences_list = line.get('gui_beneficiaire', [])
        aid_audiences = extract_mapping_values_from_list(
            AUDIENCES_DICT,
            list_of_elems=source_audiences_list,
            dict_key='name')
        return aid_audiences

    def extract_categories(self, line):
        source_categories_list = line.get('gui_tax_competence', [])
        aid_categories = extract_mapping_values_from_list(
            CATEGORIES_DICT,
            list_of_elems=source_categories_list,
            dict_key='name')
        return aid_categories

    def extract_origin_url(self, line):
        return line['url']

    def extract_contact(self, line):
        return line.get('gui_texte_gris', '')

    def extract_application_url(self, line):
        return line['gui_dematerialise_url']

    def extract_mobilization_steps(self, line):
        return [Aid.STEPS.op]

    def extract_is_call_for_project(self, line):
        return line.get('post_type') == 'ge_projet'

    def extract_recurrence(self, line):
        is_call_for_project = line.get('post_type') == 'ge_projet'
        if is_call_for_project:
            return Aid.RECURRENCES.oneoff
        return Aid.RECURRENCES.ongoing

    def extract_start_date(self, line):
        is_call_for_project = line.get('post_type') == 'ge_projet'
        if is_call_for_project:
            start_date = datetime.strptime(line.get('post_date'), '%Y-%m-%d %H:%M:%S')
            return start_date

    def extract_submission_deadline(self, line):
        is_call_for_project = line.get('post_type') == 'ge_projet'
        if is_call_for_project:
            start_date = datetime.strptime(line.get('pro_fin'), '%Y-%m-%d')
            return start_date
