import logging

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    """
    Aids from Ile de France API has wrong import_uniqueid because we use the field 'reference'
    instead of 'referenceAdministrative' field to create import_uniqueid field.

    Because of that, news aids from IDL API are created instead of an update of aids already created
    (import_uniqueid is not recognize).

    So we need to change import_uniqueid for all aids from IDL API that are already created
    in our database.

    Aids based on wrong `reference` IDL-API field have an import_unique_id beginning
    with `0000` expression
    A correct import_unique_id field for IDL import_data_source do not start by `0000`

    We can try a second clean, by :
        - searching these aids among reviewable aids
        - and merging them in published aids with the same initial_name
        and a correct import_unique_id

    """

    help = "Clean imported aids from IDL API using initial_name"

    def handle(self, *args, **options):

        from aids.models import Aid, AidWorkflow

        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.info(
            "Command clean imported aids from IDL API using initial_name field starting"
        )

        import_data_source = 4

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
