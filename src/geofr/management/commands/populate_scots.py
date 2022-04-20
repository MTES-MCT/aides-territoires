from django.core.management.base import BaseCommand
import pandas

from geofr.models import Perimeter
from geofr.utils import attach_perimeters


class Command(BaseCommand):
    """Import the list of SCoTs.

    Our data source comes from the DGALN.
    https://www.data.gouv.fr/fNr/datasets/schema-de-coherence-territoriale-scot-donnees-sudocuh-dernier-etat-des-lieux-annuel-au-31-decembre-2021/

    """

    DATA_URL = (
        "https://www.data.gouv.fr/fr/datasets/r/6e0cfffc-803d-4394-8461-af6e47795c19"
    )
    SHEET_NAME = "Communes Scot"

    def handle(self, *args, **options):
        scots = {}
        nb_created = 0
        nb_updated = 0

        # Parse the file
        df = pandas.read_excel(self.DATA_URL, sheet_name=self.SHEET_NAME, header=2)

        for _index, row in df.iterrows():
            scot_id = row["id SCoT"]
            scot_name = row["SCoT"]
            insee_code = row["Commune"]

            # Exclude the credit line at the end ("Réalisation : [...]")
            if isinstance(scot_id, int):
                if scot_id not in scots:
                    scots[scot_id] = {"name": scot_name, "communes": []}

                scots[scot_id]["communes"].append(insee_code)

        for scot_id in scots.keys():

            # id is just an integer, we use a custom code to make it unique
            scot_code = "SCOT-{}".format(scot_id)
            scot_name = scots[scot_id]["name"]

            # Create the scot perimeter
            scot, created = Perimeter.objects.update_or_create(
                scale=Perimeter.SCALES.adhoc,
                code=scot_code,
                defaults={
                    "name": scot_name,
                },
            )
            if created:
                nb_created += 1
            else:
                nb_updated += 1

            # Link the scot with the related communes
            codes = scots[scot_id]["communes"]
            attach_perimeters(scot, codes)

        self.stdout.write(
            self.style.SUCCESS(f"{nb_created} scots created, {nb_updated} updated.")
        )
