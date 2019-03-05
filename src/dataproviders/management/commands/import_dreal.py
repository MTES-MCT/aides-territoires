from datetime import date, datetime
import re
import requests
import csv
from functools import reduce

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from dataproviders.utils import content_prettify
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid


FEED_URI = 'http://aides-developpement-nouvelle-aquitaine.fr/export/dispositifs/csv?columns=key&withDates=1'
ADMIN_ID = 1

# Convert Addna's `beneficiaire` value to our value
AUDIANCES_DICT = {
    'État': None,
    'Association': Aid.AUDIANCES.association,
    'Collectivité': Aid.AUDIANCES.epci,
    'Entreprise': Aid.AUDIANCES.private_sector,
    'Particulier / Citoyen': Aid.AUDIANCES.private_person,
}


class Command(BaseCommand):
    """Import data from the DREAL data feed."""

    def handle(self, *args, **options):

        self.perimeters_cache = {}
        self.backers_cache = {}
        self.nouvelle_aquitaine = Perimeter.objects.get(
            scale=Perimeter.TYPES.region,
            code='75')

        self.beneficiaires = []

        req = requests.get(FEED_URI)
        req.encoding = 'utf-8-sig'  # We need this to take care of the bom
        csv_reader = csv.DictReader(
            req.iter_lines(decode_unicode=True),
            delimiter=';',
            lineterminator='\r\n')
        new_aids = []
        for csv_row in csv_reader:
            new_aid = self.create_aid(csv_row)
            if new_aid:
                new_aids.append(new_aid)

        print(set(self.beneficiaires))
        import pdb; pdb.set_trace()

    def create_aid(self, data):
        """Converts csv data into a valid aid object."""

        try:
            closure_date = datetime.strptime(
                data['dateCloture'], '%Y-%m-%d').date()
        except ValueError:
            closure_date = None

        if closure_date and closure_date < date.today():
            return None

        title = data['titre']
        unique_id = 'DREAL_NA_'.format(data['createdAt'])
        description = content_prettify(data['objet'])
        # publication_date = datetime.strptime(data['createdAt'])
        eligibility = data['publicsBeneficiairesDetails']
        origin_url = data['URL']
        perimeter = self.extract_perimeter(data['perimetres'])
        audiances = self.extract_audiances(data['publicsBeneficiaires'])
        backers = self.extract_backers(data['nomAttribuant'])

        # nomAttribuant -> backers
        # thematique & sousThematique -> tags
        # import url (license)
        # set search vector

        aid = Aid(
            name=title,
            author_id=ADMIN_ID,
            description=description,
            eligibility=eligibility,
            perimeter=perimeter,
            targeted_audiances=audiances,
            origin_url=origin_url,
            submission_deadline=closure_date,

            is_imported=True,
            import_uniqueid=unique_id)
        return aid

    def extract_perimeter(self, perimeters_data):
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
        # Handle the "several perimeters in the column" scenario
        perimeters = perimeters_data.split(', ')
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

    def extract_audiances(self, audiances_data):
        """Converts the `beneficiaires` column into valid audiances values.

        Cf. the ADDNA source code:
        https://github.com/DREAL-NA/aides/blob/d783fce309baf487f4ab6282dc98bccfd1c04358/app/Beneficiary.php#L28-L38
        """

        target_audiances = []
        all_audiances = []

        audiances = audiances_data.split(', ')
        for audiance in audiances:
            all_audiances.extend(audiance.split(' | '))

        for audiance in set(all_audiances):
            if audiance in AUDIANCES_DICT:
                target_audiances.append(AUDIANCES_DICT[audiance])

        return target_audiances

    def extract_backers(self, backers_data):
        """Tries to convert the `nomAttribuant` column to backers.

        Sometimes, there is a perfect match between our value and the one in
        the imported file. E.g : "Région Nouvelle - Aquitaine".

        Sometimes, we already have the backer in db, but it is spelled
        differently. E.g : "AFB - Agence Française pour la Biodiversité" vs.
        "Agence Française pour la Biodiversité".
        """

        backers = []
        attribuants = backers_data.split(', ')
        for attribuant in attribuants:
            backer = self.backers_cache.get(attribuant, None)
            if backer is None:
                # Search for an existing backer with different name versions
                possible_names = [attribuant] + attribuant.split(' - ')

                # Here, we start a request like:
                # SELECT * FROM backer WHERE
                #     name ilike <name_1> OR
                #     name ikike <name_2> OR…
                q_filters = map(lambda n: Q(name__iexact=n), possible_names)
                joined_filter = reduce(lambda q1, q2: q1 | q2, q_filters)
                found_backers = Backer.objects.filter(joined_filter)

                try:
                    backer = found_backers.get()
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        'Creating backer {}'.format(attribuant)))
                    backer = Backer.objects.create(name=attribuant)

                # if len(backers) > 1:
                #    self.stdout.write(self.style.ERROR(
                #        'Several possible backers for {}'.format(attribuant)))

            self.backers_cache[attribuant] = backer
            backers.append(backer)
        return backers
