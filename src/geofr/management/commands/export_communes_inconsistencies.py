import csv

from django.core.management.base import BaseCommand

from geofr.models import Perimeter


class Command(BaseCommand):
    """Export a CSV for communes with guessed inconsistencies."""

    def handle(self, *args, **options):
        communes = Perimeter.objects.filter(scale=Perimeter.SCALES.commune).order_by(
            "code"
        )
        with open("communes_inconsistencies.csv", "w", newline="") as csvfile:
            fieldnames = [
                "commune_pk",
                "commune_name",
                "commune_zipcodes",
                "organization_pk",
                "organization_name",
                "organization_users",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for commune in communes:
                communes_orgs = commune.organization_set.filter(
                    organization_type=["commune"]
                )
                if communes_orgs.count() > 1:
                    for commune_org in communes_orgs.all():
                        row = {
                            "commune_pk": commune.pk,
                            "commune_name": commune.name,
                            "commune_zipcodes": ", ".join(
                                zipcode for zipcode in commune.zipcodes
                            ),
                            "organization_pk": commune_org.pk,
                            "organization_name": commune_org.name,
                            "organization_users": ", ".join(
                                [str(user) for user in commune_org.user_set.all()]
                            ),
                        }
                        writer.writerow(row)
