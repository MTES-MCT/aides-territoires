import logging
from django.core.management.base import BaseCommand
from geofr.services.import_data_from_api_geo import import_communes_extra_data

from geofr.services.populate import (
    populate_communes,
    populate_countries,
    populate_epcis,
    populate_overseas,
    populate_regions,
    populate_departments,
)


class Command(BaseCommand):
    """
    Import the list of 'Collectivités locales' based on the files
    provided by Etalab.
    """

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Importing countries..."))
        result = populate_countries()
        self.stdout.write(
            self.style.SUCCESS(
                f"{result['created']} created, {result['updated']} updated."
            )
        )

        self.stdout.write(self.style.NOTICE("Importing regions..."))
        result = populate_regions()
        self.stdout.write(
            self.style.SUCCESS(
                f"{result['created']} created, {result['updated']} updated."
            )
        )

        self.stdout.write(self.style.NOTICE("Importing departments..."))
        result = populate_departments()
        self.stdout.write(
            self.style.SUCCESS(
                f"{result['created']} created, {result['updated']} updated."
            )
        )

        self.stdout.write(self.style.NOTICE("Importing communes..."))
        result = populate_communes()
        self.stdout.write(
            self.style.SUCCESS(
                f"{result['created']} created, {result['updated']} updated."
            )
        )

        self.stdout.write(self.style.NOTICE("Importing EPCIs..."))
        result = populate_epcis()
        self.stdout.write(
            self.style.SUCCESS(
                f"{result['created']} created, {result['updated']} updated."
            )
        )

        self.stdout.write(self.style.NOTICE("Importing overseas..."))
        populate_overseas()
        self.stdout.write(self.style.NOTICE("Done..."))

        self.stdout.write(self.style.NOTICE("Importing extra data..."))
        logger = logging.getLogger("console_log")
        result = import_communes_extra_data(logger)
        self.stdout.write(
            self.style.NOTICE(
                f"Population imported for {result['nb_treated']} communes."
            )
        )

        if len(result["not_found"]):
            self.stdout.write(
                self.style.ERROR(
                    "The following communes were not found in Aides-territoires:"
                )
            )
            for commune in result["not_found"]:
                self.stdout.write(self.style.ERROR(f"* {commune}"))
