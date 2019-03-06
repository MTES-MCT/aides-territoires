import os
from datetime import date, datetime
import re
import requests
import csv

from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from django.contrib.postgres.search import TrigramSimilarity

from dataproviders.utils import content_prettify
from dataproviders.management.commands.base import BaseImportCommand
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid


FEED_URI = 'http://aides-developpement-nouvelle-aquitaine.fr/export/dispositifs/csv?columns=key&withDates=1&sep=pipe'
ADMIN_ID = 1

# Convert Addna's `beneficiaire` value to our value
AUDIANCES_DICT = {
    'État': None,
    'Association': Aid.AUDIANCES.association,
    'Collectivité': Aid.AUDIANCES.epci,
    'Entreprise': Aid.AUDIANCES.private_sector,
    'Particulier / Citoyen': Aid.AUDIANCES.private_person,
}


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
        self.backers_cache = {}
        self.nouvelle_aquitaine = Perimeter.objects.get(
            scale=Perimeter.TYPES.region,
            code='75')
        self.beneficiaires = []

        super().handle(*args, **options)

    def line_should_be_processed(self, line):
        deadline = self.extract_submission_deadline(line)
        return deadline is None or deadline > date.today()

    def extract_import_uniqueid(self, line):
        unique_id = 'DREAL_NA_{}'.format(line['createdAt'])
        return unique_id

    def extract_author_id(self, line):
        return ADMIN_ID

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

    def extract_tags(self, line):
        tags = [line['sousThematique']]
        return tags

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

    def extract_targeted_audiances(self, line):
        """Converts the `beneficiaires` column into valid audiances values.

        Cf. the ADDNA source code:
        https://github.com/DREAL-NA/aides/blob/d783fce309baf487f4ab6282dc98bccfd1c04358/app/Beneficiary.php#L28-L38
        """

        audiances_data = line['publicsBeneficiaires']
        target_audiances = []
        all_audiances = []

        audiances = audiances_data.split('<|>')
        for audiance in audiances:
            all_audiances.extend(audiance.split(' | '))

        for audiance in set(all_audiances):
            if audiance in AUDIANCES_DICT:
                target_audiances.append(AUDIANCES_DICT[audiance])

        return target_audiances

    def extract_backers(self, line):
        """Tries to convert the `nomAttribuant` column to backers.

        Sometimes, there is a perfect match between our value and the one in
        the imported file. E.g : "Région Nouvelle - Aquitaine".

        Sometimes, we already have the backer in db, but it is spelled
        differently. E.g : "AFB - Agence Française pour la Biodiversité" vs.
        "Agence Française pour la Biodiversité".
        """

        backers_data = line['nomAttribuant']

        backers = []
        attribuants = backers_data.split('<|>')
        for attribuant in attribuants:
            backer = self.backers_cache.get(attribuant, None)
            if backer is None:

                # Since there are some differences between the spelling of
                # the same backers between us and the search data, we
                # perform a trigram similarity search.
                found_backers = Backer.objects \
                    .annotate(sml=TrigramSimilarity('name', attribuant)) \
                    .filter(sml__gt=0.8) \
                    .order_by('-sml')
                try:
                    backer = found_backers[0]
                except IndexError:
                    self.stdout.write(self.style.ERROR(
                        'Creating backer {}'.format(attribuant)))
                    backer = Backer.objects.create(name=attribuant)

            self.backers_cache[attribuant] = backer
            backers.append(backer)
        return backers
