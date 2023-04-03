from django.core.management.base import BaseCommand
import logging

from geofr.services.import_insee_data import import_communes_typology_data


class Command(BaseCommand):
    """
    This script imports data about if a commune is
    rural or urban.

    Data source: https://www.insee.fr/fr/statistiques/5039991?sommaire=5040030
    """

    def handle(self, *args, **options):
        logger = logging.getLogger("console_log")
        logger.setLevel(logging.INFO)

        result = import_communes_typology_data()
        logger.info(f"Typology data imported for {result['nb_treated']} communes.")
