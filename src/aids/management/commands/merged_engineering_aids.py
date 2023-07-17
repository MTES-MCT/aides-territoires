import logging
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Update aid_type fields"

    def handle(self, *args, **options):
        from aids.models import Aid
        from search.models import SearchPage
        from alerts.models import Alert

        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.info("Command update aids_types started")

        logger.info("Update aids started")

        aids = Aid.objects.all()

        for aid in aids:
            if aid.aid_types is not None:
                if Aid.TYPES.technical_engineering in aid.aid_types:
                    aid.aid_types.append(Aid.TYPES.strategic_engineering)
                    aid.aid_types.append(Aid.TYPES.diagnostic_engineering)
                    aid.aid_types.remove(Aid.TYPES.technical_engineering)
                    aid.save()

                if Aid.TYPES.legal_engineering in aid.aid_types:
                    aid.aid_types.append(Aid.TYPES.administrative_engineering)
                    aid.aid_types.append(Aid.TYPES.legal_and_regulatory_engineering)
                    aid.aid_types.remove(Aid.TYPES.legal_engineering)
                    aid.save()

        logger.info("Update aids finished")

        logger.info("Update alerts started")

        alerts = Alert.objects.all()

        for alert in alerts:
            if "aid_type=technical_engineering" in alert.querystring:
                new_querystring = alert.querystring.replace(
                    "aid_type=technical_engineering",
                    "aid_type=strategic_engineering&aid_type=diagnostic_engineering",
                )
                alert.querystring = new_querystring
                alert.save()
            if "aid_type=legal_engineering" in alert.querystring:
                new_querystring = alert.querystring.replace(
                    "aid_type=legal_engineering",
                    "aid_type=administrative_engineering&aid_type=legal_and_regulatory_engineering",
                )
                alert.querystring = new_querystring
                alert.save()
        logger.info("Update alerts finished")

        logger.info("Update portals started")

        portals = SearchPage.objects.all()

        for portal in portals:
            if "aid_type=technical_engineering" in portal.search_querystring:
                new_querystring = portal.search_querystring.replace(
                    "aid_type=technical_engineering",
                    "aid_type=strategic_engineering&aid_type=diagnostic_engineering",
                )
                portal.search_querystring = new_querystring
                portal.save()
            if "aid_type=legal_engineering" in portal.search_querystring:
                new_querystring = portal.search_querystring.replace(
                    "aid_type=legal_engineering",
                    "aid_type=administrative_engineering&aid_type=legal_and_regulatory_engineering",
                )
                portal.search_querystring = new_querystring
                portal.save()
        logger.info("Update portals finished")
