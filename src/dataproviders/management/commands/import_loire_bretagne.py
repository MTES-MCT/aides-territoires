# flake8: noqa
import os
from datetime import datetime
import re
import csv

from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify
from dataproviders.management.commands.base import BaseImportCommand
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid


ADMIN_ID = 1

# Convert Addna's `beneficiaire` value to our value
AUDIENCES_DICT = {
    'État': None,
    'Association': Aid.AUDIENCES.association,
    'Collectivité': Aid.AUDIENCES.epci,
    'Entreprise': Aid.AUDIENCES.private_sector,
    'Particulier / Citoyen': Aid.AUDIENCES.private_person,
}

AIDES_URL = 'https://aides-redevances.eau-loire-bretagne.fr/home/aides/lessentiel-des-aides/aides-mode-demploi.html'

LOIRE_BRETAGNE_PERIMETER_CODE = '04'
LOIRE_BRETAGNE_FINANCER_ID = 74  # "Agence de l'Eau Loire-Bretagne"


class Command(BaseImportCommand):
    """Import data from the Loire-Bretagne water agency data file.

    The file was manually built so this script will probably be ran only once.
    """

    def add_arguments(self, parser):
        parser.add_argument('data-file', nargs=1, type=str)

    def fetch_data(self, **options):
        data_file = os.path.abspath(options['data-file'][0])
        with open(data_file) as csvfile:
            csv_reader = csv.DictReader(
                csvfile,
                delimiter=';',
                lineterminator='\r\n')
            for csv_line in csv_reader:
                yield csv_line

    def handle(self, *args, **options):

        self.perimeter_loire_bretagne = Perimeter.objects.get(
            scale=Perimeter.TYPES.basin,
            code=LOIRE_BRETAGNE_PERIMETER_CODE)
        self.backer_loire_bretagne = Backer.objects.get(
            id=LOIRE_BRETAGNE_FINANCER_ID)
        super().handle(*args, **options)

    def line_should_be_processed(self, line):
        return True

    def extract_author_id(self, line):
        return ADMIN_ID

    def extract_import_uniqueid(self, line):
        unique_id = 'EAU_LB_{}'.format(self.extract_reference(line))
        return unique_id

    def extract_import_data_url(self, line):
        return AIDES_URL

    def extract_import_share_licence(self, line):
        return IMPORT_LICENCES.unknown

    def extract_start_date(self, line):
        try:
            start_date = datetime.strptime(
                line["Date d'ouverture"], '%m/%d/%Y').date()
        except ValueError:
            start_date = None
        return start_date

    def extract_submission_deadline(self, line):
        try:
            closure_date = datetime.strptime(
                line['Date de clôture '], '%m/%d/%Y').date()
        except ValueError:
            closure_date = None
        return closure_date

    def extract_name(self, line):
        title = line["Nom de l'aide"]
        return title

    def extract_description(self, line):
        # The reference and description are merged with no space in the
        # same column. Why? I don't know.
        val = line["Référence + Description"]
        aid_re = r'^[A-Z]{3}_\d_\d'
        if re.match(aid_re, val):
            raw_description = val[7:]
        else:
            raw_description = ' '.join(val.split(' ')[1:])
        return content_prettify(raw_description)

    def extract_reference(self, line):
        # See method above for rationale
        val = line["Référence + Description"]
        aid_re = r'^[A-Z]{3}_\d_\d'
        if re.match(aid_re, val):
            ref = val[:7]
        else:
            ref = val.split(' ')[0]
        return ref

    def extract_origin_url(self, line):
        return AIDES_URL

    def extract_perimeter(self, line):
        return self.perimeter_loire_bretagne

    def extract_targeted_audiences(self, line):
        audiences = []
        if line['Collectivités']:
            audiences += ['commune', 'epci', 'unions', 'department', 'region']
        if line['Entreprises']:
            audiences += ['private_sector']
        if line['Agriculture']:
            audiences += ['farmer']
        if line['Associations']:
            audiences += ['association']
        if line['Particuliers']:
            audiences += ['private_person']
        return audiences

    def extract_financers(self, line):
        return [self.backer_loire_bretagne]

    def extract_recurrence(self, line):
        return Aid.RECURRENCES.oneoff

    def extract_aid_types(self, line):
        return [Aid.TYPES.grant]

    def extract_subvention_rate(self, line):
        value = line["taux de sub"]
        if value:
            rate = [30, 70]
        else:
            rate = None

        return rate

    def extract_contact(self, line):
        return '''
        <p>
        Pour toute information complémentaire,
        <a href="https://agence.eau-loire-bretagne.fr/home/agence-de-leau/fonctionnement-de-lagence-de-leau/agence-eau-loire-bretagne-un-siege-et-5-delegations.html">
        vous pouvez contacter votre direction régionale</a>.
        </p>
        '''

    def extract_eligibility(self, line):
        return ''
