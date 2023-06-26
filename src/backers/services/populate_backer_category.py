import os
import csv
import logging

from django.db import transaction

from backers.models import BackerGroup, BackerCategory, BackerSubCategory

logger = logging.getLogger("console_log")

BACKER_SUBCATEGORY_CSV_PATH = (
    os.path.dirname(os.path.realpath(__file__)) + "/data/backer_subcategory.csv"
)


@transaction.atomic
def create_backer_category() -> None:
    """
    Create the backer's category if doesn't exists
    """

    backer_category_all = []
    nb_created = 0
    nb_updated = 0

    logger.debug("Parsing file and create backer_categories")

    with open(BACKER_SUBCATEGORY_CSV_PATH) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for index, row in enumerate(reader):
            backer_category = row["Catégorie"]
            backer_category, created = BackerCategory.objects.get_or_create(
                name=backer_category,
            )
            if created:
                nb_created += 1
                backer_category_all.append(backer_category)
            else:
                nb_updated += 1

    logger.info(f"{nb_created} categories created, {nb_updated} updated.")


@transaction.atomic
def create_and_attached_backer_subcategory() -> None:
    """
    Create the backer's subcategory if doesn't exists
    And attached the backer's subcategory to a backer's category
    """

    backer_subcategory_all = []
    nb_created = 0
    nb_updated = 0

    logger.debug("Parsing file and create backer_subcategories")

    with open(BACKER_SUBCATEGORY_CSV_PATH) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for index, row in enumerate(reader):
            backer_subcategory = row["Sous-catégorie"]
            backer_category = BackerCategory.objects.get(name=row["Catégorie"])
            backer_subcategory, created = BackerSubCategory.objects.get_or_create(
                name=backer_subcategory, category=backer_category
            )
            if created:
                nb_created += 1
                backer_subcategory_all.append(backer_subcategory)
            else:
                nb_updated += 1

    logger.info(f"{nb_created} subcategories created, {nb_updated} updated.")


@transaction.atomic
def attached_backer_group_to_subcategory() -> None:
    """
    Aattached the backer's subcategory to a backer's group
    """
    nb_updated = 0

    logger.debug("Get backer_group object and attached backer_subcategory")

    with open(BACKER_SUBCATEGORY_CSV_PATH) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for index, row in enumerate(reader):
            backer_subcategory_name = row["Sous-catégorie"]
            backer_subcategory = BackerSubCategory.objects.get(
                name=backer_subcategory_name
            )
            backer_group_name = row["Groupe AT"]

            try:
                backer_group = BackerGroup.objects.filter(
                    name=backer_group_name,
                )
                backer_group.update(subcategory=backer_subcategory)
                nb_updated += 1
            except Exception as e:
                print(backer_group_name)
                print(e)

    logger.info(f"{nb_updated} backer groups updated")
