import logging
import csv
import codecs
import requests
from contextlib import closing

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    """
    Aids from Ile de France API has wrong import_uniqueid because we use the field 'reference'
    instead of 'referenceAdministrative' field to create import_uniqueid field.

    Because of that, news aids from IDL API are created instead of an update of aids already created
    (import_uniqueid is not recognize).

    So we need to change import_uniqueid for all aids from IDL API that are already created
    in our database.
    Our partner give us a file with the couple 'reference' and 'referenceAdministrative'.
    This file is not complete so we are not able to fix all aids in our database.
    A manual clean will be needed to finalize this task.
    """

    help = "Clean imported aids from IDL API : Update the import_uniqueid field from table's file"

    def add_arguments(self, parser):
        parser.add_argument("--url")

    def handle(self, *args, **options):

        from aids.models import Aid

        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.info("Command clean imported aids from IDL API starting")

        csv_url = options["url"]
        import_data_source = 4
        imported_aids = Aid.objects.filter(
            import_data_source=import_data_source,
        )

        if csv_url:
            with closing(requests.get(csv_url, stream=True)) as response:
                csv_content = codecs.iterdecode(response.iter_lines(), "utf-8")
                aids_reader = csv.DictReader(csv_content, delimiter=";")
                aids_updated = 0
                for row in enumerate(aids_reader):
                    reference_administrative = (
                        f"IDF_{row[1]['referenceAdministrative']}"
                    )
                    reference = f"IDF_{row[1]['reference']}"
                    for aid in imported_aids:
                        if aid.import_uniqueid == reference:
                            try:
                                aid.import_uniqueid = reference_administrative
                                aid.save()
                                aids_updated += 1
                                logger.info(f"aid with pk {aid.pk} updated")
                            except Exception as e:
                                logger.info(
                                    f"{e} : aid {aid.pk} and import_uniqueid={aid.import_uniqueid} not updated"  # noqa
                                )

                logger.info(f"{aids_updated} aids reference updated from file")
