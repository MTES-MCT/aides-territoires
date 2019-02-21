from datetime import date, datetime
import re
import requests
import csv

from django.core.management.base import BaseCommand

from dataproviders.utils import content_prettify
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid


FEED_URI = 'http://aides-developpement-nouvelle-aquitaine.fr/export/dispositifs/csv?columns=key&withDates=1'
ADMIN_ID = 1


class Command(BaseCommand):
    """Import data from the DREAL data feed."""

    def handle(self, *args, **options):

        self.perimeters_cache = {}
        self.nouvelle_aquitaine = Perimeter.objects.get(
            scale=Perimeter.TYPES.region,
            code='75')

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

        # thematique & sousThematique -> tags
        # nomAttribuant -> backers
        # publicsBeneficiaires -> targeted_audiances
        # import url (license)


        aid = Aid(
            name=title,
            author_id=ADMIN_ID,
            description=description,
            eligibility=eligibility,
            perimeter=perimeter,
            origin_url=origin_url,
            submission_deadline=closure_date,

            is_imported=True,
            import_uniqueid=unique_id
        )
        import pdb; pdb.set_trace()
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
        if re.match(r'^\d{2}', perimeter_name):
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
