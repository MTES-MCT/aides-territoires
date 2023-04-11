import logging
import os
import csv
import codecs
import requests
from contextlib import closing

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Clean imported aids : Update the import_uniqueid field and delete duplicated imported aids"

    def add_arguments(self, parser):
        parser.add_argument("--import_data_source_id")
        parser.add_argument("--url")
        parser.add_argument("--file")

    def handle(self, *args, **options):
        from aids.models import Aid, AidWorkflow, AidProject, SuggestedAidProject

        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.info("Command clean imported aids starting")

        csv_url = options["url"]
        csv_file = options["file"]

        import_data_source = int(options["import_data_source_id"])

        imported_aids = Aid.objects.filter(
            import_data_source=import_data_source,
        )

        logger.info(f"{imported_aids.count()} imported_aids")

        if csv_url:
            with closing(requests.get(csv_url, stream=True)) as response:
                csv_content = codecs.iterdecode(response.iter_lines(), "utf-8")
                aids_reader = csv.DictReader(csv_content, delimiter=";")
        elif csv_file:
            csv_path = os.path.abspath(csv_file)
            with open(csv_path) as csv_file_open:
                aids_reader = csv.DictReader(csv_file_open, delimiter=";")
                aids_updated = 0
                for row in enumerate(aids_reader):
                    referenceAdministrative = f"IDF_{row[1]['referenceAdministrative']}"
                    reference = f"IDF_{row[1]['reference']}"
                    for aid in imported_aids:
                        if aid.import_uniqueid == reference:
                            logger.info(
                                f"aid with pk {aid.pk} and reference = {reference}"
                            )
                            try:
                                aid.import_uniqueid = referenceAdministrative
                                aid.save()
                                aids_updated += 1
                                logger.info(f"aid with pk {aid.pk} updated")
                            except Exception as e:
                                logger.info(
                                    f"Exception {e} : aid with pk {aid.pk} and reference = {reference} not updated"
                                )

                        logger.info(f"{aids_updated} aids reference updated from file")

        aids_published = Aid.objects.filter(
            import_data_source=import_data_source,
            status=AidWorkflow.states.published.name,
        ).exclude(import_uniqueid__icontains="0000")

        aids_reviewable = Aid.objects.filter(
            import_data_source=import_data_source,
            status=AidWorkflow.states.reviewable.name,
            import_uniqueid__icontains="0000",
        )

        for aid_reviewable in aids_reviewable:
            for aid_published in aids_published:
                if aid_reviewable.name_initial == aid_published.name_initial:
                    aid_published.import_uniqueid = (
                        f"bis-{aid_reviewable.import_uniqueid}"
                    )
                    aid_published.save()

                    aid_reviewable.import_uniqueid = (
                        f"duplicated-{aid_reviewable.import_uniqueid}"
                    )
                    aid_reviewable.status = AidWorkflow.states.merged
                    aid_reviewable.save()

                    aid_published.import_uniqueid = str(
                        aid_published.import_uniqueid.partition("bis-")[2]
                    )
                    aid_published.save()
                    logger.info(
                        f"aid with pk {aid_published.pk} updated from initial_name"
                    )
