import csv
import logging
import codecs
import requests
from contextlib import closing
from datetime import datetime

from geofr.models import Perimeter
from projects.models import ValidatedProject
from organizations.models import Organization
from aids.models import Aid


def create_validated_project(row):
    logger = logging.getLogger("console_log")

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
                project_name=row["projet"],
                aid_name=row["appelation"],
                budget=int(row["cout_total_ht"].replace(",", "")),
                date_obtained=datetime.strptime(row["annee"], "%Y"),
                amount_obtained=int(row["subvention_accordee"].replace(",", "")),
                organization=organization,
            )
            if aid.exists():
                logger.info("aid found")
                validatedproject.aid_linked = aid.first()
                validatedproject.aid_name = aid.first().name
                validatedproject.save()
        except Exception as e:
            print(e)
            print(row["projet"])
    else:
        logger.info("perimeter not found")


def import_validated_projects(csv_file=None, csv_url=None):
    logger = logging.getLogger("console_log")
    logger.info("Command import_validated_projects starting")

    if csv_url:
        with closing(requests.get(csv_url, stream=True)) as response:
            csv_content = codecs.iterdecode(response.iter_lines(), "utf-8")
            projects_reader = csv.DictReader(csv_content, delimiter=",")
            for index, row in enumerate(projects_reader):
                create_validated_project(row)
    elif csv_file:
        with open(csv_file) as csv_file_open:
            projects_reader = csv.DictReader(csv_file_open, delimiter=";")
            for index, row in enumerate(projects_reader):
                create_validated_project(row)
