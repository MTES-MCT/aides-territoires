from datetime import datetime

from django.utils import timezone

from dataproviders.constants import IMPORT_LICENCES
from dataproviders.management.commands.base import CrawlerImportCommand
from dataproviders.scrapers.rmc import RMCSpider
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid


ADMIN_ID = 1

BASIN_RHONE_MED_CODE = "06"
BASIN_CORSE_CODE = "12"
FINANCER_ID = 53  # "Agence de l'eau Rhône-Méditerranée-Corse"


ELIGIBILITY_TXT = """
Rendez-vous sur le site de l'agence de l'eau Rhône Méditaranée Corse pour
obtenir les informations relatives aux conditions d'éligibilité.
"""


# We consider that all RMC aids have the same deadline
RMC_DEADLINE = timezone.make_aware(datetime(2025, 12, 31))


class Command(CrawlerImportCommand):
    """Import data from the eaurmc.fr site."""

    SPIDER_CLASS = RMCSpider

    def populate_cache(self, *args, **options):
        self.perimeter = (
            Perimeter.objects.filter(scale=Perimeter.SCALES.basin)
            .filter(code=BASIN_RHONE_MED_CODE)
            .get()
        )

        self.financer = Backer.objects.get(id=FINANCER_ID)

    def extract_author_id(self, line):
        return ADMIN_ID

    def extract_import_uniqueid(self, line):
        return line["uniqueid"]

    def extract_origin_url(self, line):
        return line["current_url"]

    def extract_import_data_url(self, line):
        return line["current_url"]

    def extract_import_share_licence(self, line):
        return IMPORT_LICENCES.unknown

    def extract_name(self, line):
        return line["title"]

    def extract_description(self, line):
        return line["description"]

    def extract_eligibility(self, line):
        return ELIGIBILITY_TXT

    def extract_perimeter(self, line):
        return self.perimeter

    def extract_financers(self, line):
        return [self.financer]

    def extract_targeted_audiences(self, line):
        return [Aid.AUDIENCES.epci]

    def extract_submission_deadline(self, line):
        return RMC_DEADLINE
