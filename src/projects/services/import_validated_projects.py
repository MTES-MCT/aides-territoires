import os
import csv
import logging
from datetime import datetime

from geofr.models import Perimeter
from projects.models import ValidatedProject
from organizations.models import Organization
from aids.models import Aid


def import_validated_projects():
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
                    validatedproject = ValidatedProject.objects.create(
                        unknown_aid=row["appelation"],
                        unknown_project=row["projet"],
                        budget=int(row["cout_total_ht"].replace(",", "")),
                        date_obtention=datetime.strptime(row["annee"], "%Y"),
                        amount_obtained=int(
                            row["subvention_accordee"].replace(",", "")
                        ),
                    )
                    validatedproject.organizations.add(organization)
                    validatedproject.save()
                    if aid.exists():
                        logger.info("aid found")
                        validatedproject.aid = aid.first()
                        validatedproject.save()
                except Exception as e:
                    print(e)
                    print(row["projet"])
