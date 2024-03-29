import csv
import logging
import codecs
import hashlib
import requests
from contextlib import closing
from datetime import datetime
from io import TextIOWrapper

from django.utils import timezone

from aids.models import Aid
from backers.models import Backer
from geofr.models import Perimeter
from organizations.models import Organization
from projects.models import ValidatedProject


def create_validated_project(row, logger=None):
    """
    The row is only imported if the following criteria are met
    - the project has a name
    - the project's perimeter exists
    - the field 'cout_total_ht' has a numeric value
    - the field 'subvention_accordee' has a numeric value
    """
    if not logger:
        logger = logging.getLogger("console_log")

    project_name = row["projet"]
    organization_name = row["beneficiaire"]

    department_code = row["departement"]
    if len(department_code) == 1:
        department_code = f"0{department_code}"

    perimeter = Perimeter.objects.filter(
        name__iexact=organization_name,
        scale=1,
        departments__contains=[department_code],
    ).first()

    budget = clean_numeric_input(row["cout_total_ht"], logger)
    amount_obtained = clean_numeric_input(row["subvention_accordee"], logger)

    if perimeter is None:
        logger.debug(f"Perimeter not found for {organization_name}.")
    elif project_name and budget and amount_obtained:
        # Force the organization name to use the same case as the perimeter
        organization_name = perimeter.name

        try:
            aid = Aid.objects.filter(
                name__icontains=row["appelation"],
                perimeter__code=department_code,
            )

            organization = Organization.objects.filter(
                name__iexact=organization_name,
                perimeter=perimeter,
                organization_type=["commune"],
            ).first()

            if organization is None:
                organization = Organization.objects.create(
                    name=organization_name,
                    perimeter=perimeter,
                    organization_type=["commune"],
                    is_imported=True,
                )

            if len(project_name) <= 255:
                project_description = ""
            else:
                project_description = project_name
                project_name = project_name[:254] + "…"

            year = row["annee"]
            date_obtained = datetime.strptime(year, "%Y")
            date_obtained = timezone.make_aware(date_obtained)

            aid_name = row["appelation"]
            financer_name = row["porteur_name"]

            # Manually setting a unique import_uniqueid because get_or_create fails at
            # detecting duplicates over so many fields
            import_unique_string = "⋅".join(
                [project_name, aid_name, financer_name, str(amount_obtained), year]
            ).lower()
            import_uniqueid = hashlib.sha256(
                import_unique_string.encode("utf-8")
            ).hexdigest()

            validatedproject, created = ValidatedProject.objects.update_or_create(
                import_uniqueid=import_uniqueid,
                defaults={
                    "project_name": project_name,
                    "aid_name": aid_name,
                    "financer_name": financer_name,
                    "amount_obtained": amount_obtained,
                    "date_obtained": date_obtained,
                    "description": project_description,
                    "budget": budget,
                    "organization": organization,
                },
            )
            if created:
                logger.debug("Project created")
            else:
                logger.debug("Project already in database")
            if aid.exists():
                validatedproject.aid_linked = aid.first()
                validatedproject.aid_name = aid.first().name
                validatedproject.save()
            if Backer.objects.filter(id=row["porteur_id"]).exists():
                financer = Backer.objects.get(id=row["porteur_id"])
                validatedproject.financer_linked = financer
                validatedproject.save()
        except Exception as e:
            logger.error(f"Error while importing row {row['projet']}")
            logger.error(e)


def import_validated_projects(logger=None, csv_file=None, csv_url=None):
    if not logger:
        logger = logging.getLogger("console_log")

    logger.info("Command import_validated_projects starting")

    if csv_url:
        with closing(requests.get(csv_url, stream=True)) as response:
            csv_content = codecs.iterdecode(response.iter_lines(), "utf-8")
            projects_reader = csv.DictReader(csv_content, delimiter=";")
            for index, row in enumerate(projects_reader):
                if index % 1000 == 0:
                    logger.info(f"{index} rows treated")
                create_validated_project(row, logger)
    elif csv_file:
        csv_file_open = TextIOWrapper(csv_file, encoding="utf-8")
        projects_reader = csv.DictReader(csv_file_open, delimiter=";")
        for index, row in enumerate(projects_reader):
            if index % 1000 == 0:
                logger.info(f"{index} rows treated")
            create_validated_project(row, logger)


def clean_numeric_input(input_string: str, logger) -> int | None:
    """
    The numbers used in the source come from an OCR and need cleaning
    """
    common_wrong_values = ["abandon", "###", "-"]

    if any(i in input_string for i in common_wrong_values):
        return None

    input_string = input_string.replace(" ", "")  # normal space
    input_string = input_string.replace(" ", "")  # non-breakable space
    input_string = input_string.replace(",", "")
    input_string = input_string.replace("€", "")
    input_string = input_string.replace("E", "")
    input_string = input_string.replace("*", "")
    input_string = input_string.replace("o", "0")

    try:
        if len(input_string):
            return int(input_string)
        else:
            return None
    except Exception as e:
        logger.warning(f"clean_numeric_input error: {e}")
        return None
