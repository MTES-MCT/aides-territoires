import os
import requests
import json

from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify
from dataproviders.management.commands.base import BaseImportCommand
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid


FEED_URI = 'https://www.bpifrance.fr/offers/export/innovation/'
ADMIN_ID = 1

TYPES_DICT = {
    'Avance récupérable': Aid.TYPES.recoverable_advance,
    'Innovation': None,
    'Accompagnement': Aid.TYPES.financial,
    'Subvention': Aid.TYPES.grant,
    'Prêt': Aid.TYPES.loan,
    'Investissement': Aid.TYPES.other,
    'Garantie': Aid.TYPES.other,
}

SOURCE_URL = 'https://www.bpifrance.fr/'
CONTACT_URL = 'https://www.bpifrance.fr/Contactez-nous'


class Command(BaseImportCommand):
    """Import data from the BPI data feed."""

    def add_arguments(self, parser):
        parser.add_argument('data-file', nargs='?', type=str)

    def fetch_data(self, **options):
        if options['data-file']:
            data_file = os.path.abspath(options['data-file'])
            data = json.load(open(data_file))
            for line in data['data']:
                yield line

        else:
            req = requests.get(FEED_URI)
            req.encoding = 'utf-8-sig'  # We need this to take care of the bom
            data = json.loads(req.text)
            for line in data['data']:
                yield line

    def handle(self, *args, **options):

        self.france = Perimeter.objects.get(
            scale=Perimeter.TYPES.country,
            code='FRA')
        self.bpi = Backer.objects.get(slug='bpi-france')

        super().handle(*args, **options)

    def line_should_be_processed(self, line):
        return True

    def extract_author_id(self, line):
        return ADMIN_ID

    def extract_import_uniqueid(self, line):
        unique_id = 'BPI_{}'.format(line['ref_partenaire'])
        return unique_id

    def extract_import_data_url(self, line):
        return SOURCE_URL

    def extract_import_share_licence(self, line):
        return IMPORT_LICENCES.unknown

    def extract_submission_deadline(self, line):
        return None

    def extract_name(self, line):
        title = line['title']
        return title

    def extract_description(self, line):
        desc_0 = content_prettify('<p>{}</p>'.format(
            line['baseline']))
        desc_1 = content_prettify('<p>Nous (la BPI) {}</p>'.format(
            line['introduction_us']))
        desc_2 = content_prettify(line['we'])
        description = desc_0 + desc_1 + desc_2
        return description

    def extract_eligibility(self, line):
        elig_1 = content_prettify('<p>Vous {}</p>'.format(
            line['introduction_you']))
        elig_2 = content_prettify(line['you'])
        eligibility = elig_1 + elig_2
        return eligibility

    def extract_origin_url(self, line):
        origin_url = line['linkoffer']
        return origin_url

    def extract_perimeter(self, line):
        """Converts the "perimetres" column value into a Perimeter object.

        The column can hold some fairly standard values:
         * Europe
         * National
         * Nouvelle - Aquitaine
         * 33 - Gironde

        Some are slightly more exotic:
         * Marais Poitevin
         * International

        Others seems to be unique values manually filled:
         * Communes couvertes par un PPRN prescrit ou approuvé
         * Territoires à risques d’inondation importants

        Also, the column can hold several values (e.g several departments).

        We try to match the perimeter by name. In case we can find a valid
        candidate, or if several values are present, we default to
        the region of Nouvelle - Aquitaine.

        """
        return self.france

    def extract_targeted_audiences(self, line):
        return [Aid.AUDIENCES.private_sector]

    def extract_financers(self, line):
        return [self.bpi]

    def extract_contact(self, line):
        return '<p><a href="{}">Contactez directement la BPI</a></p>'.format(
            CONTACT_URL)

    def extract_aid_types(self, line):
        types = line['type'].split(';')
        aid_types = [TYPES_DICT.get(t, None) for t in types]
        return [t for t in aid_types if t]

    def extract_recurrence(self, line):
        return Aid.RECURRENCES.ongoing
