import os
import csv

from django.core.management.base import BaseCommand

from geofr.models import Perimeter


# Source for those values is a buried table in a 70 pages pdf here:
# http://www.sandre.eaufrance.fr/urn.php?urn=urn:sandre:dictionnaire:COM::entite:CircAdminBassin:ressource:3.0:::html
DRAINAGE_BASINS = {
    '01': 'Artois-Picardie',
    '02': 'Rhin-Meuse',
    '03': 'Seine-Normandie',
    '04': 'Loire-Bretagne',
    '05': 'Adour-Garonne',
    '06': 'Rhône-Méditérranée',
    '07': 'Guadeloupe',
    '08': 'Martinique',
    '09': 'Guyane',
    '10': 'Réunion',
    '11': 'Mayotte',
    '12': 'Corse',
}

OVERSEAS_BASINS = ('07', '08', '09', '10', '11')


class Command(BaseCommand):
    """Import the list of drainage basins.

    This task is highly inefficient (no batch saving, updating every row one by
    one, etc.) but it will be ran only once, so it's not a big deal.

    The file can be downloaded at this address:
    http://www.data.eaufrance.fr/jdd/176f23a8-8f4f-4eab-9f23-411e7490bbc5
    « Télécharger les communes administratives 2018 - Format CSV -
    Listing des communes - Format CSV »

    The most accurate description we have about this file structure is an email
    conversation with L. Coudercy from AFB:

        - le code bassin DCE (A, B2 ...) : il s'agit des codes européens des
        bassins, utilisés pour le rapportage : une agence peut être concerné
        par plusieurs codes (dans le nord et l'est de la France, sinon c'est
        unique)
        - le code eu district (EU3, EU33, ...) : c'est à peu prêt la même
        chose (je dois t'avouer que je ne sais pas exactement ce que c'est)
        - le numCircAdminBassin : (1, 2, ...) correspond aux circonscriptions
        administratives de bassin
        - le CdComiteBassin (2528, 1463, ...) correspond aux organisations que
        sont les comités de bassin
        Attention : il y a une circonscription administrative de bassin (et
        donc un comité de bassin) par agence, sauf pour Rhône Méditerranée
        Corse, où la Corse a sa propre circonscription administrative de bassin
        (codes D-6-2256 pour Rhône Méditerranée, et E-12-2252 pour Corse) !
        Par contre, pour les DOM, il n'y a pas de comité de bassin (d'où des
        FR000011, par exemple)
        Il est donc fort probable que pour la Corse les aides soient
        différentes de celles de Rhône Méditerranée, puisque c'est le
        comité de bassin qui les vote !
        Tu peux donc te baser sur le numéro de circonscription de bassin.
    """

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=str)

    def handle(self, *args, **options):

        # Create basin perimeters
        basin_to_commune = {}
        basin_to_epci = {}
        for code, basin_name in DRAINAGE_BASINS.items():
            Perimeter.objects.get_or_create(
                scale=Perimeter.TYPES.basin,
                code=code,
                name=basin_name,
                is_overseas=code in OVERSEAS_BASINS)
            basin_to_commune[code] = list()
            basin_to_epci[code] = list()

        # Import data from csv file
        csv_path = os.path.abspath(options['csv_file'][0])
        with open(csv_path) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                commune_code = row['CdCommune']
                basin_code = row['NumCircAdminBassin']
                basin_to_commune[basin_code].append(commune_code)

        # Update communes with the correct basin codes
        for basin_code in basin_to_commune.keys():
            Perimeter.objects \
                .filter(scale=Perimeter.TYPES.commune) \
                .filter(code__in=basin_to_commune[basin_code]) \
                .update(basin=basin_code)

        # Update epcis with basin codes
        epcis = Perimeter.objects \
            .filter(scale=Perimeter.TYPES.commune) \
            .values_list('epci', 'basin')
        for epci_code, basin_code in epcis:
            basin_to_epci[basin_code].append(epci_code)

        for basin_code in basin_to_epci.keys():
            Perimeter.objects \
                .filter(scale=Perimeter.TYPES.epci) \
                .filter(code__in=basin_to_epci[basin_code]) \
                .update(basin=basin_code)
