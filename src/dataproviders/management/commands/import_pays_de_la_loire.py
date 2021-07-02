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
from dataproviders.utils import content_prettify
from dataproviders.management.commands.base import BaseImportCommand
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid


ADMIN_ID = 1

DATA_SOURCE = DataSource.objects \
    .prefetch_related('perimeter', 'backer') \
    .get(pk=2)

OPENDATA_URL = 'https://data.paysdelaloire.fr/explore/dataset/234400034_referentiel-aides-paysdelaloirefr/information/'
FEED_ROWS = 1000

AUDIENCES_DICT = {}
AUDIENCES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/pays_de_la_loire_audiences_mapping.csv'
SOURCE_COLUMN_NAME = 'Bénéficiaires Pays de la Loire'
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

TYPES_DICT = {}
TYPES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/pays_de_la_loire_types_mapping.csv'
SOURCE_COLUMN_NAME = 'Types Pays de la Loire'
AT_COLUMN_NAMES = ['Types AT 1']
with open(TYPES_MAPPING_CSV_PATH) as csv_file:
    csvreader = csv.DictReader(csv_file, delimiter=",")
    for index, row in enumerate(csvreader):
        if row[AT_COLUMN_NAMES[0]]:
            TYPES_DICT[row[SOURCE_COLUMN_NAME]] = []
            for column in AT_COLUMN_NAMES:
                if row[column]:
                    audience = next(choice[0] for choice in Aid.TYPES if choice[1] == row[column])
                    TYPES_DICT[row[SOURCE_COLUMN_NAME]].append(audience)

CALL_FOR_PROJECT_LIST = [
    'Appel à projets',
    'Appel à manifestations d\'intérêt'
]

RECURRENCE_DICT = {
    'Temporaire': Aid.RECURRENCE.oneoff,
    'Permanent': Aid.RECURRENCE.ongoing,
}


class Command(BaseImportCommand):
    """Import data from the Pays de la Loire Open Data plateform.
    ~300 aids as of November 2020
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
        unique_id = 'PDLL_{}'.format(line['intervention_id'])
        return unique_id

    def extract_import_data_url(self, line):
        return OPENDATA_URL

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_name(self, line):
        title = line['aide_nom'][:180]
        # title = line['aid_objet_court'][:180]
        return title

    def extract_description(self, line):
        # desc_1 & desc_2 already have <p></p> tags
        desc_1 = content_prettify(line.get('aid_objet', ''))
        desc_2 = content_prettify(line.get('aid_operations_ei', ''))
        description = desc_1 + desc_2
        return description

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_eligibility(self, line):
        # eligibility already has <p></p> tags
        eligibility = content_prettify(line.get('aidconditions', ''))
        return eligibility

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    # def extract_origin_url(self, line):
    #     """
    #     The origin url is not provided.
    #     We construct it, but there may be some errors.
    #     """
    #     aid_name = line['aide_nom'].replace(' à ', ' ').replace(' À ', ' ')
    #     aid_slug = slugify(aid_name)
    #     return 'https://www.paysdelaloire.fr/les-aides/' + aid_slug

    def extract_application_url(self, line):
        application_url = line.get('source_lien', '')
        return application_url

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process: "Associations;Collectivités - Institutions - GIP;Entreprises"
        Split the string, loop on the values and match to our AUDIENCES
        """
        audiences = line.get('aid_benef', '').split(';')
        aid_audiences = []
        for audience in audiences:
            if audience in AUDIENCES_DICT:
                aid_audiences.extend(AUDIENCES_DICT.get(audience, []))
            else:
                self.stdout.write(self.style.ERROR(f'Audience {audience} not mapped'))
        return aid_audiences

    def extract_aid_types(self, line):
        """
        Exemple of string to process: "Avance remboursable;Prêt"
        """
        types = line.get('type_de_subvention', '').split(';')
        aid_types = []
        for type_item in types:
            if type_item in TYPES_DICT:
                aid_types.extend(TYPES_DICT.get(type_item, []))
            else:
                self.stdout.write(self.style.ERROR(f'Type {type_item} not mapped'))
        return aid_types

    def extract_is_call_for_project(self, line):
        is_call_for_project = line['type_aide'] in CALL_FOR_PROJECT_LIST
        return is_call_for_project

    def extract_recurrence(self, line):
        if line.get('temporalite', None):
            recurrence = RECURRENCE_DICT.get(line['temporalite'], None)
            return recurrence
        return None

    def extract_start_date(self, line):
        if line['temporalite'] == 'Temporaire':
            if line.get('date_de_debut', None):
                start_date = datetime.strptime(line['date_de_debut'], '%Y-%m-%d')
                return start_date
        return None

    def extract_submission_deadline(self, line):
        if line['temporalite'] == 'Temporaire':
            if line.get('date_de_fin', None):
                submission_deadline = datetime.strptime(line['date_de_fin'], '%Y-%m-%d').date()
                return submission_deadline
        return None

    # def extract_subvention_comment(self, line):
    #     montant_min = line.get('montantintervmini', '-')
    #     montant_max = line.get('montant_interv_max', '-')
    #     subvention_comment = 'montantintervmini / montant_interv_max' + ' : ' + str(montant_min) + ' / ' + str(montant_max)
    #     return subvention_comment

    def extract_contact(self, line):
        direction = line.get('direction', '')
        service = line.get('service', '')
        pole = line.get('pole', '')
        contact_1 = '<p>' + '<br />'.join([direction, service, pole]) + '</p>'
        contact_name = line.get('contact_prenom', '') + line.get('contact_nom', '')
        contact_email = line.get('contact_email', '')
        contact_phone = line.get('tel', '')
        contact_2 = '<p>' + '<br />'.join([contact_name, contact_email, contact_phone]) + '</p>'
        contact_detail = content_prettify(line.get('informations_contact', ''))
        return contact_1 + contact_2 + contact_detail

    def extract_project_examples(self, line):
        """Use the project_examples textfield to store metadata"""
        content = ''
        metadata = {
            "aid_objet_court": "Aide object court",
            "thematique_libelle": "Thématique(s)",
            "ss_thematique_libelle": "Sous thématique(s)",
            "aide_seniors": "Aide séniors",
            "aide_femmes": "Aide femmes",
            "aide_handicapes": "Aide handicapés",
            "aide_jeunes": "Aide jeunes",
            "aid_demandeurs": "Aide demandeurs",
            "conditions_de_versement": "Conditions de versement",
            "type_procedure": "Type procédure",
            "actif": "Actif",
            "montantintervmini": "Montant interv mini",
            "montant_interv_max": "Montant interv max",
        }
        for elem in metadata:
            if line.get(elem, None):
                content += '<strong>{}</strong> : {}<br /><br />'.format(metadata[elem], line[elem])
        return content
