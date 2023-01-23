import os
import csv
import logging
from datetime import datetime

from geofr.models import Perimeter
from projects.models import Project
from organizations.models import Organization
from aids.models import Aid, AidProject

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Add multiple aids to a project from a distant csv"

    def handle(self, *args, **options):
        """
        If a perimeter has data['beneficiaire'] for name and is a commune
            - We search for an aid in database with name contains data['appelation']
                and with perimeter'code is data['departement']
            - We create an organization with data['beneficiaire'] as a name
            and perimeter as perimeter
            - We create a project
            - We create a relation between the aid and the project
        """

        validated_projects_csv_path = os.path.abspath("projects_validated.csv")
        with open(validated_projects_csv_path) as csv_file:
            csvreader = csv.DictReader(csv_file, delimiter=";")
            logger = logging.getLogger("console_log")
            logger.info("Command import_validated_projects starting")
            for index, row in enumerate(csvreader):
                if Perimeter.objects.filter(
                    name=row["beneficiaire"],
                    scale=1,
                    departments__contains=[row["departement"]],
                ).exists():
                    logger.info("perimeter found")
                    try:
                        perimeter = Perimeter.objects.get(
                            name=row["beneficiaire"],
                            scale=1,
                            departments__contains=[row["departement"]],
                        )
                        aid = Aid.objects.filter(
                            name__icontains=row["appelation"],
                            perimeter__code=row["departement"],
                        )
                        if Organization.objects.filter(
                            name=row["beneficiaire"],
                            perimeter=perimeter,
                            organization_type=["commune"],
                        ).exists():
                            organization = Organization.objects.filter(
                                name=row["beneficiaire"],
                                perimeter=perimeter,
                                organization_type=["commune"],
                            ).first()
                        else:
                            organization = Organization.objects.create(
                                name=row["beneficiaire"],
                                perimeter=perimeter,
                                organization_type=["commune"],
                                is_imported=True,
                            )
                        project = Project.objects.create(
                            name=row["projet"],
                            final_budget=int(row["cout_total_ht"].replace(",", "")),
                            is_imported=True,
                            is_public=True,
                            status=Project.STATUS.published,
                            step=Project.PROJECT_STEPS.validated,
                        )
                        project.organizations.add(organization)
                        project.save()
                        if aid.exists():
                            logger.info("aid found")
                            AidProject.objects.create(
                                project=project,
                                aid=aid.first(),
                                aid_requested=True,
                                aid_obtained=True,
                                date_obtained=datetime.strptime(row["annee"], "%Y"),
                                date_requested=datetime.strptime(row["annee"], "%Y"),
                                amount_obtained=int(
                                    row["subvention_accordee"].replace(",", "")
                                ),
                            )
                        else:
                            logger.info("aid unknown")
                            AidProject.objects.create(
                                project=project,
                                aid_unknown=row["appelation"],
                                aid_requested=True,
                                aid_obtained=True,
                                date_obtained=datetime.strptime(row["annee"], "%Y"),
                                date_requested=datetime.strptime(row["annee"], "%Y"),
                                amount_obtained=int(
                                    row["subvention_accordee"].replace(",", "")
                                ),
                            )
                    except Exception as e:
                        print(e)
                        print(row["projet"])
