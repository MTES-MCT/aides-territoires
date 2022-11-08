from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Merge duplicated imported aids"

    def add_arguments(self, parser):
        parser.add_argument("--backer_id")
        parser.add_argument("--import_data_source_id")

    def handle(self, *args, **options):
        from aids.models import Aid

        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.debug("Command merge duplicated imported aids starting")

        backer = options["backer_id"]
        import_data_source = options["import_data_source"]

        old_aids = Aids.objects.filter(
            financers=backer,
            is_imported=True,
            import_data_source=None,
        )

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
                old_aid.update(                    
                )
                duplicated_aid.delete()