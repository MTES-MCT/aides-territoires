import os
from datetime import date, datetime
import re
import requests
import csv

from django.contrib.postgres.search import TrigramSimilarity

from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify
from dataproviders.management.commands.base import BaseImportCommand
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid


FEED_URI = 'http://aides-developpement-nouvelle-aquitaine.fr/export/dispositifs/csv?columns=key&withDates=1&sep=pipe'  # noqa
ADMIN_ID = 1

# Convert Addna's `beneficiaire` value to our value
AUDIENCES_DICT = {
    'État': None,
    'Association': Aid.AUDIENCES.association,
    'Collectivité': Aid.AUDIENCES.epci,
    'Entreprise': Aid.AUDIENCES.private_sector,
    'Particulier / Citoyen': Aid.AUDIENCES.private_person,
}

ADDNA_URL = 'http://aides-dd-na.fr/'

NOUVELLE_AQUITAINE_PERIMETER_CODE = '75'


class Command(BaseImportCommand):
    """Import data from the DREAL data feed."""

    def add_arguments(self, parser):
        parser.add_argument('data-file', nargs='?', type=str)

    def fetch_data(self, **options):
        if options['data-file']:
            data_file = os.path.abspath(options['data-file'])
            with open(data_file) as csvfile:
                csv_reader = csv.DictReader(
                    csvfile,
                    delimiter=';',
                    lineterminator='\r\n')
                for csv_line in csv_reader:
                    yield csv_line

        else:
            req = requests.get(FEED_URI)
            req.encoding = 'utf-8-sig'  # We need this to take care of the bom
            csv_reader = csv.DictReader(
                req.iter_lines(decode_unicode=True),
                delimiter=';',
                lineterminator='\r\n')

            for csv_line in csv_reader:
                yield csv_line

    def handle(self, *args, **options):

        self.perimeters_cache = {}
        self.financers_cache = {}
        self.nouvelle_aquitaine = Perimeter.objects.get(
            scale=Perimeter.SCALES.region,
            code=NOUVELLE_AQUITAINE_PERIMETER_CODE)
        self.beneficiaires = []

        super().handle(*args, **options)

    def line_should_be_processed(self, line):
        deadline = self.extract_submission_deadline(line)
        return deadline is None or deadline > date.today()

    def extract_author_id(self, line):
        return ADMIN_ID

    def extract_import_uniqueid(self, line):
        unique_id = 'DREAL_NA_{}'.format(line['createdAt'])
        return unique_id

    def extract_import_data_url(self, line):
        return ADDNA_URL

    def extract_import_share_licence(self, line):
        return IMPORT_LICENCES.openlicence20

    def extract_submission_deadline(self, line):
        try:
            closure_date = datetime.strptime(
                line['dateCloture'], '%Y-%m-%d').date()
        except ValueError:
            closure_date = None
        return closure_date

    def extract_name(self, line):
        title = line['titre']
        return title

    def extract_description(self, line):
        description = content_prettify(line['objet'])
        return content_prettify(description)

    def extract_eligibility(self, line):
        eligibility = line['publicsBeneficiairesDetails']
        return content_prettify(eligibility)

    def extract_origin_url(self, line):
        origin_url = line['URL']
        return origin_url

    # def extract_tags(self, line):
    #     tags = [line['sousThematique']]
    #     return tags

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
        perimeters_data = line['perimetres']

        # Handle the "several perimeters in the column" scenario
        perimeters = perimeters_data.split('<|>')
        if len(perimeters) > 1:
            perimeter_name = 'Nouvelle - Aquitaine'
        else:
            perimeter_name = perimeters[0]

        if perimeter_name == 'National':
            perimeter_name = 'France'

        # The ADDNA prefixes departments (and only departments) with their
        # INSEE code. Let's get rid of it.
        if re.match(r'^\d{2} - ', perimeter_name):
            perimeter_name = perimeter_name.split(' - ')[1]

        # Is this a known perimeter?
        if perimeter_name in self.perimeters_cache:
            perimeter = self.perimeters_cache[perimeter_name]
        else:
            try:
                perimeter = Perimeter.objects.get(name=perimeter_name)
            except Perimeter.DoesNotExist:
                perimeter = self.nouvelle_aquitaine
            self.perimeters_cache[perimeter_name] = perimeter

        return perimeter

    def extract_targeted_audiences(self, line):
        """Converts the `beneficiaires` column into valid audiences values.

        Cf. the ADDNA source code:
        https://github.com/DREAL-NA/aides/blob/d783fce309baf487f4ab6282dc98bccfd1c04358/app/Beneficiary.php#L28-L38
        """

        audiences_data = line['publicsBeneficiaires']
        target_audiences = []
        all_audiences = []

        audiences = audiences_data.split('<|>')
        for audience in audiences:
            all_audiences.extend(audience.split(' | '))

        for audience in set(all_audiences):
            if audience in AUDIENCES_DICT:
                target_audiences.append(AUDIENCES_DICT[audience])

        return target_audiences

    def extract_financers(self, line):
        """Tries to convert the `nomAttribuant` column to financers.

        Sometimes, there is a perfect match between our value and the one in
        the imported file. E.g : "Région Nouvelle - Aquitaine".

        Sometimes, we already have the financer in db, but it is spelled
        differently. E.g : "AFB - Agence Française pour la Biodiversité" vs.
        "Agence Française pour la Biodiversité".
        """

        financers_data = line['nomAttribuant']

        financers = []
        attribuants = financers_data.split('<|>')
        for attribuant in attribuants:
            financer = self.financers_cache.get(attribuant, None)
            if financer is None:

                # Since there are some differences between the spelling of
                # the same financers between us and the search data, we
                # perform a trigram similarity search.
                found_financers = Backer.objects \
                    .annotate(sml=TrigramSimilarity('name', attribuant)) \
                    .filter(sml__gt=0.8) \
                    .order_by('-sml')
                try:
                    financer = found_financers[0]
                except IndexError:
                    self.stdout.write(self.style.ERROR(
                        'Creating financer {}'.format(attribuant)))
                    financer = Backer.objects.create(name=attribuant)

            self.financers_cache[attribuant] = financer
            financers.append(financer)
        return financers
