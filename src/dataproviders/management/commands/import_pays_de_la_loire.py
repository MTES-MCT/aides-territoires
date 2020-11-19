# flake8: noqa
import os
from datetime import datetime
import requests
import json

from django.conf import settings
from django.utils.text import slugify

from dataproviders.utils import content_prettify
from dataproviders.management.commands.base import BaseImportCommand
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid


OPENDATA_URL = 'https://data.paysdelaloire.fr/explore/dataset/234400034_referentiel-aides-paysdelaloirefr/information/'
FEED_URI = 'https://data.paysdelaloire.fr/api/records/1.0/search/'
FEED_ROWS = 1000
FEED_PARAMS = {
    'dataset': '234400034_referentiel-aides-paysdelaloirefr',
    'rows': FEED_ROWS,
    'facet': 'type_aide',
    'facet': 'ss_thematique',
    'facet': 'thematique_libelle',
    'facet': 'ss_thematique_libelle',
    'facet': 'type_de_subvention',
    'facet': 'conditions_de_versement',
    'facet': 'aid_benef',
    'facet': 'type_procedure',
    'facet': 'direction',
    'facet': 'service',
    'facet': 'pole',
    'apikey': settings.API_KEY_PAYS_DE_LA_LOIRE
}

AID_URL_PREFIX = 'https://www.paysdelaloire.fr/les-aides/'

AUDIENCES_COLLECTIVITE_LIST = [
    Aid.AUDIENCES.commune,
    Aid.AUDIENCES.epci,
    Aid.AUDIENCES.department,
    Aid.AUDIENCES.public_cies,
    Aid.AUDIENCES.public_org
]
AUDIENCES_DICT = {
    'Association': Aid.AUDIENCES.association,
    # 'Collectivités - Institutions - GIP': AUDIENCES_COLLECTIVITE_LIST,  # managed seperately
    'Entreprise': Aid.AUDIENCES.private_sector,
    'Etablissements ESR - Organismes de recherche': Aid.AUDIENCES.researcher,
    'Jeunes': Aid.AUDIENCES.private_person,
    'Lycées et centres de formation': Aid.AUDIENCES.public_org,
    'Particuliers': Aid.AUDIENCES.private_person,
}

TYPES_DICT = {
    'Aide': Aid.TYPES.grant,
    'Accompagnement': Aid.TYPES.technical,
    'Aide en nature': Aid.TYPES.other,
    'Appel à manifestations d\'intérêt': Aid.TYPES.grant,
    'Avance remboursable': Aid.TYPES.recoverable_advance,
    'Garantie': Aid.TYPES.other,
    'Prêt': Aid.TYPES.loan,
    'Prêt d\'honneur': Aid.TYPES.loan,
    'Service': Aid.TYPES.other,
    'Subvention': Aid.TYPES.grant,
}

CALL_FOR_PROJECT_LIST = [
    'Appel à projets',
    'Appel à manifestations d\'intérêt'
]

RECURRENCE_DICT = {
    'Temporaire': Aid.RECURRENCE.oneoff,
    'Permanent': Aid.RECURRENCE.ongoing,
}

PAYS_DE_LA_LOIRE_PERIMETER_CODE = '52'
PAYS_DE_LA_LOIRE_FINANCER_NAME = 'Conseil régional des Pays de la Loire'


class Command(BaseImportCommand):
    """Import data from the Pays de la Loire Open Data plateform.
    ~300 aids as of November 2020
    """

    def add_arguments(self, parser):
        parser.add_argument('data-file', nargs='?', type=str)

    def fetch_data(self, **options):
        if options['data-file']:
            data_file = os.path.abspath(options['data-file'])
            data = json.load(open(data_file))
            for line in data['data']:
                yield line
        else:
            req = requests.get(FEED_URI, params=FEED_PARAMS)
            req.encoding = 'utf-8-sig'  # We need this to take care of the bom
            data = json.loads(req.text)
            self.stdout.write('Total number of aids: {}'.format(data['nhits']))
            if data['nhits'] > FEED_ROWS:
                self.stdout.write(self.style.ERROR(
                    'Only fetching {} aids, but there are {} aids'.format(FEED_ROWS, data['nhits'])))
            self.stdout.write('Number of aids processing: {}'.format(len(data['records'])))
            for line in data['records']:
                yield line['fields']

    def handle(self, *args, **options):

        self.pays_de_la_loire_perimeter = Perimeter.objects \
            .filter(scale=Perimeter.TYPES.region) \
            .filter(code=PAYS_DE_LA_LOIRE_PERIMETER_CODE) \
            .get()
        self.pays_de_la_loire_financer = Backer.objects.get(name=PAYS_DE_LA_LOIRE_FINANCER_NAME)

        super().handle(*args, **options)

    def line_should_be_processed(self, line):
        return True

    def extract_import_uniqueid(self, line):
        unique_id = 'PDLL_{}'.format(line['intervention_id'])
        return unique_id

    def extract_import_data_url(self, line):
        return OPENDATA_URL

    def extract_import_share_licence(self, line):
        return Aid.IMPORT_LICENCES.unknown

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
        return [self.pays_de_la_loire_financer]

    def extract_eligibility(self, line):
        # eligibility already has <p></p> tags
        eligibility = content_prettify(line.get('aidconditions', ''))
        return eligibility

    def extract_perimeter(self, line):
        return self.pays_de_la_loire_perimeter

    def extract_origin_url(self, line):
        """
        The origin url is not provided.
        We construct it, but there may be some errors.
        """
        aid_name = line['aide_nom'].replace(' à ', ' ').replace(' À ', ' ')
        aid_slug = slugify(aid_name)
        return AID_URL_PREFIX + aid_slug

    def extract_application_url(self, line):
        application_url = line.get('source_lien', None)
        return application_url

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process: "Associations;Collectivités - Institutions - GIP;Entreprises"
        Split the string, loop on the values and match to our AUDIENCES
        """
        targeted_audiences = line.get('aid_benef', '').split(';')
        aid_targeted_audiences = [AUDIENCES_DICT.get(t, None) for t in targeted_audiences]
        # manage custom case
        if 'Collectivités - Institutions - GIP' in targeted_audiences:
            aid_targeted_audiences += AUDIENCES_COLLECTIVITE_LIST
        return [t for t in aid_targeted_audiences if t]

    def extract_aid_types(self, line):
        """
        Exemple of string to process: "Avance remboursable;Prêt"
        """
        types = line.get('type_de_subvention', '').split(';')
        aid_types = [TYPES_DICT.get(t, None) for t in types]
        return [t for t in aid_types if t]

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
