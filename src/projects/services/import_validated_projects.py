import csv
import logging
import codecs
import requests
from contextlib import closing
from datetime import datetime
from io import TextIOWrapper

from geofr.models import Perimeter
from projects.models import ValidatedProject
from organizations.models import Organization
from aids.models import Aid
from backers.models import Backer


def create_validated_project(row):
    logger = logging.getLogger("console_log")

    if Perimeter.objects.filter(
        name=row["beneficiaire"],
        scale=1,
        departments__contains=[row["departement"]],
    ).exists():
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
            if len(row["projet"]) <= 255:
                project_name = row["projet"]
                project_description = ""
            else:
                project_name = row["projet"][:254] + "…"
                project_description = row["projet"]
            validatedproject = ValidatedProject.objects.create(
                project_name=project_name,
                description=project_description,
                aid_name=row["appelation"],
                budget=int(row["cout_total_ht"].replace(",", "")),
                date_obtained=datetime.strptime(row["annee"], "%Y"),
                amount_obtained=int(row["subvention_accordee"].replace(",", "")),
                organization=organization,
                financer_name=row["porteur_name"],
            )
            logger.info("project created")
            if aid.exists():
                validatedproject.aid_linked = aid.first()
                validatedproject.aid_name = aid.first().name
                validatedproject.save()
            if Backer.objects.filter(id=row["porteur_id"]).exists():
                financer = Backer.objects.get(id=row["porteur_id"])
                validatedproject.financer_linked = financer
                validatedproject.save()
        except Exception as e:
            print(e)
            print(row["projet"])


def import_validated_projects(csv_file=None, csv_url=None):
    logger = logging.getLogger("console_log")
    logger.info("Command import_validated_projects starting")

    if csv_url:
        with closing(requests.get(csv_url, stream=True)) as response:
            csv_content = codecs.iterdecode(response.iter_lines(), "utf-8")
            projects_reader = csv.DictReader(csv_content, delimiter=";")
            for index, row in enumerate(projects_reader):
                create_validated_project(row)
    elif csv_file:
        csv_file_open = TextIOWrapper(csv_file, encoding="utf-8")
        projects_reader = csv.DictReader(csv_file_open, delimiter=";")
        for index, row in enumerate(projects_reader):
            create_validated_project(row)
