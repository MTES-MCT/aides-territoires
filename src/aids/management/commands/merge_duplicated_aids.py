import logging
from django.utils import timezone
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Merge duplicated imported aids"

    def add_arguments(self, parser):
        parser.add_argument("--backer_id")
        parser.add_argument("--import_data_source_id")

    def handle(self, *args, **options):
        from aids.models import Aid, AidWorkflow, AidProject, SuggestedAidProject
        from dataproviders.models import DataSource

        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.info("Command merge duplicated imported aids starting")

        backer = int(options["backer_id"])
        import_data_source = int(options["import_data_source_id"])
        import_data_source_instance = DataSource.objects.get(pk=import_data_source)

        old_aids = Aid.objects.filter(
            financers=backer,
            import_data_source__isnull=True,
        )

        logger.info(f"{old_aids.count()} old_aids")

        merged_aids = 0
        for old_aid in old_aids:
            if Aid.objects.filter(
                name=old_aid.name,
                is_imported=True,
                import_data_source=import_data_source,
                financers=backer 
            ).exists():
                duplicated_aid = Aid.objects.filter(
                    name=old_aid.name,
                    is_imported=True,
                    import_data_source=import_data_source,
                    financers=backer
                ).first()

                logger.info(f"duplicated aid exists {duplicated_aid.pk=}-{old_aid.pk=}")
                try:
                    old_aid.name_initial=duplicated_aid.name_initial
                    old_aid.short_title=duplicated_aid.short_title
                    old_aid.description=duplicated_aid.description
                    old_aid.author=duplicated_aid.author
                    old_aid.project_examples=duplicated_aid.project_examples
                    old_aid.eligibility=duplicated_aid.eligibility
                    old_aid.mobilization_steps=duplicated_aid.mobilization_steps
                    old_aid.origin_url=duplicated_aid.origin_url
                    old_aid.targeted_audiences=duplicated_aid.targeted_audiences
                    old_aid.aid_types=duplicated_aid.aid_types
                    old_aid.destinations=duplicated_aid.destinations
                    old_aid.start_date=duplicated_aid.start_date
                    old_aid.predeposit_date=duplicated_aid.predeposit_date
                    old_aid.submission_deadline=duplicated_aid.submission_deadline
                    old_aid.subvention_rate=duplicated_aid.subvention_rate
                    old_aid.subvention_comment=duplicated_aid.subvention_comment
                    old_aid.recoverable_advance_amount=duplicated_aid.recoverable_advance_amount
                    old_aid.loan_amount=duplicated_aid.loan_amount
                    old_aid.contact=duplicated_aid.contact
                    old_aid.contact_email=duplicated_aid.contact_email
                    old_aid.contact_phone=duplicated_aid.contact_phone
                    old_aid.contact_detail=duplicated_aid.contact_detail
                    old_aid.recurrence=duplicated_aid.recurrence
                    old_aid.is_call_for_project=duplicated_aid.is_call_for_project
                    old_aid.date_updated=timezone.now()
                    old_aid.in_france_relance=duplicated_aid.in_france_relance
                    old_aid.european_aid=duplicated_aid.european_aid
                    old_aid.author_notification=duplicated_aid.author_notification
                    old_aid.is_imported=duplicated_aid.is_imported
                    old_aid.import_uniqueid=f"bis-{duplicated_aid.import_uniqueid}"
                    old_aid.import_data_source=duplicated_aid.import_data_source
                    old_aid.import_data_url=duplicated_aid.import_data_url
                    old_aid.import_share_licence=duplicated_aid.import_share_licence
                    old_aid.import_data_mention=duplicated_aid.import_data_mention
                    old_aid.import_last_access=duplicated_aid.import_last_access
                    old_aid.import_raw_object=duplicated_aid.import_raw_object
                    old_aid.import_raw_object_calendar=duplicated_aid.import_raw_object_calendar
                    old_aid.import_raw_object_temp=duplicated_aid.import_raw_object_temp
                    old_aid.import_raw_object_temp_calendar=duplicated_aid.import_raw_object_temp_calendar
                    old_aid.search_vector_unaccented=duplicated_aid.search_vector_unaccented
                    old_aid.clone_m2m(duplicated_aid)
                    old_aid.save()

                    duplicated_aid.status = AidWorkflow.states.merged
                    duplicated_aid.import_data_source_id = f"duplicated-{duplicated_aid.import_data_source_id}"
                    duplicated_aid.save()

                    old_aid.import_data_source_id = str(old_aid.import_data_source_id.partition("bis-")[2])
                    old_aid.save()

                    if duplicated_aid.projects is not None:
                        for project in duplicated_aid.projects.all():
                            aidproject = AidProject.objects.get(aid=duplicated_aid.pk, project=project.pk)
                            aidproject.aid = old_aid
                            aidproject.save()

                        for suggested_project in duplicated_aid.suggested_projects.all():
                            suggested_aidproject = SuggestedAidProject.objects.get(aid=duplicated_aid.pk, project=suggested_project.pk)
                            suggested_aidproject.aid = old_aid
                            suggested_aidproject.save()

                    merged_aids += 1
                    logger.info(f"duplicated aid {duplicated_aid.pk} merged in old aid {old_aid.pk}")
                except Exception as e:
                    print(e)
        logger.info(f"{merged_aids} merged aids")
