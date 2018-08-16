import os
import json
from datetime import datetime
from django.core.management.base import BaseCommand

from aids.models import Aid
from backers.models import Backer


TIME_FMT = '%a %b %d %Y %H:%M:%S %Z%z (UTC)'


class Command(BaseCommand):
    """Imports old data into the new base.

    In the project's first version, a no-sql mongo database was used. This
    script is made to import this data into today's django model.

    Note: since this script is designed to be run once and then forgotten,
    tests and quality are left to the minimum.
    """

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs=1, type=str)

    def handle(self, *args, **options):

        json_file = os.path.abspath(options['json_file'][0])
        json_data = json.load(open(json_file))
        for datum in json_data:
            self.import_aid(datum)

    def import_aid(self, data):
        backer, _ = Backer.objects.get_or_create(name=data['structurePorteuse'])

        aid = Aid()
        aid.name = data['nom']
        aid.description = data['description']
        aid.author_id = 1
        aid.backer = backer
        aid.eligibility = data['criteresEligibilite']
        aid.application_perimeter = self.get_application_perimeter(data)  # XXX
        aid.mobilization_steps = self.get_mobilization_steps(data)
        aid.url = data['lien']
        aid.minimal_population = data['populationMin']
        aid.maximal_population = data['populationMax']
        aid.targeted_audiances = self.get_audiances(data)
        aid.targeted_audiances_detail = data['beneficiairesAutre']
        aid.is_funding = data['type'] == 'financement'
        aid.aid_types = self.get_types(data)
        aid.aid_types_detail = data['formeDeDiffusionAutre']
        aid.destinations = self.get_destinations(data)
        aid.destinations_detail = data['destinationAutre']
        aid.thematics = self.get_thematics(data)

        if data['dateDebut']:
            aid.start_date = datetime.strptime(
                data['dateDebut'], TIME_FMT)

        if 'datePredepot' in data and data['datePredepot']:
            aid.predeposit_date = datetime.strptime(
                data['datePredepot'], TIME_FMT)

        if data['dateEcheance']:
            aid.submission_deadline = datetime.strptime(
                data['dateEcheance'], TIME_FMT)

        aid.subvention_rate = data['tauxSubvention']
        aid.contact_detail = data['contact']
        aid.publication_status = self.get_status(data)
        aid.open_to_third_party = data['demandeTiersPossible'] is not None

        aid.save()

    def get_application_perimeter(self, data):
        pass

    def get_mobilization_steps(self, data):
        pass

    def get_audiances(self, data):
        pass

    def get_types(self, data):
        pass

    def get_destinations(self, data):
        pass

    def get_thematics(self, data):
        pass

    def get_status(self, data):
        pass
