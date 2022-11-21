import csv

from django.core.management.base import BaseCommand

from geofr.models import Perimeter


class Command(BaseCommand):
    """Export a CSV for EPCI with guessed inconsistencies."""

    def handle(self, *args, **options):
        epcis = Perimeter.objects.filter(scale=Perimeter.SCALES.epci).order_by("code")
        with open("epci_inconsistencies.csv", "w", newline="") as csvfile:
            fieldnames = [
                "epci_pk",
                "epci_name",
                "organization_pk",
                "organization_name",
                "organization_users",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for epci in epcis:
                epcis_orgs = epci.organization_set.filter(organization_type=["epci"])
                if epcis_orgs.count() > 1:
                    for epci_org in epcis_orgs.all():
                        row = {
                            "epci_pk": epci.pk,
                            "epci_name": epci.name,
                            "organization_pk": epci_org.pk,
                            "organization_name": epci_org.name,
                            "organization_users": ", ".join(
                                [str(user) for user in epci_org.user_set.all()]
                            ),
                        }
                        writer.writerow(row)
