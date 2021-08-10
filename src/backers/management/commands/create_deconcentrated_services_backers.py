# flake8: noqa
from django.core.management.base import BaseCommand

from backers.models import Backer
from geofr.constants import OVERSEAS_REGIONS
from geofr.models import Perimeter


SERVICES = [
    'Ademe — Direction régionale',
    'Banque des Territoires — Direction régionale',
    'Préfecture de région',
    'Direction régionale de l\'Alimentation, de l\'Agriculture et de la Forêt (DRAAF)',
    'Direction régionale des Affaires culturelles (DRAC)',
    "Direction régionale des Entreprises, de la Concurrence, de la Consommation, du Travail et de l’Emploi (DIRECCTE)",
    "Direction régionale de l’environnement, de l’aménagement et du logement (DREAL)",
    "Direction régionale des Finances publiques (DRFiP)",
    "Région académique",
    "Direction régionale de la Jeunesse, des Sports et de la Cohésion sociale (DRJSCS)",
    "Délégation régionale à la recherche et à la technologie (DRRT)",
    "Agence régionale de santé (ARS)",
]


class Command(BaseCommand):
    """Create backers entries for regional deconcentrated services."""

    def handle(self, *args, **options):
        confirm = input('This command is meant to run in production only '
                        'once.\nAre you sure you know what you\'re doing?\n')
        if confirm != 'yes':
            return

        regions = Perimeter.objects \
            .filter(scale=Perimeter.SCALES.region) \
            .exclude(code__in=OVERSEAS_REGIONS)

        backers = []
        for region in regions:
            for service in SERVICES:
                backers.append(Backer(
                    name='{} — {}'.format(service, region.name)))

        results = Backer.objects.bulk_create(backers)
        self.stdout.write(self.style.SUCCESS(
            '{} backers created'.format(len(results))
        ))
