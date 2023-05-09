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

    Aids based on wrong `reference` IDL-API field have an import_unique_id not beginning
    with `0000` expression
    A correct import_unique_id field for IDL import_data_source start by `0000`

    We can try a second clean, by :
        - searching aids with correct import_uniqueid among reviewable aids
        - findind an aid with the same initial_name among published aids
        - saving the published corresponding aid with the import_uniqueid of reviewable aid
        - changing reviewable aid status by merged status

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

        # Select only published aids with a wrong import_uniqueid
        aids_published = Aid.objects.filter(
            import_data_source=import_data_source,
            status=AidWorkflow.states.published.name,
        ).exclude(import_uniqueid__icontains="0000")

        # Select only reviewable aids with a good import_uniqueid
        aids_reviewable = Aid.objects.filter(
            import_data_source=import_data_source,
            status=AidWorkflow.states.reviewable.name,
            import_uniqueid__icontains="0000",
        )

        # Search a match between name_initial of aid_reviewable and name_initial of aid_published
        # if so use import_unique_id of aid_reviewable for import_unique_id of aid_published
        # and change status of aid_reviewable.
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
