from django.core.management.base import BaseCommand

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

        self.stdout.write(self.style.NOTICE("Importing overseas..."))
        result = populate_overseas()
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
