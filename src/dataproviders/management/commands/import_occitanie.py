from datetime import datetime

from dataproviders.constants import IMPORT_LICENCES
from dataproviders.management.commands.base import CrawlerImportCommand
from dataproviders.scrapers.occitanie import OccitanieSpider
from geofr.models import Perimeter
from backers.models import Backer


OPENDATA_URL = "https://data.laregion.fr/explore/dataset/aides-et-appels-a-projets-de-la-region-occitanie/information/"  # noqa

ELIGIBILITY_TXT = """Consultez la page de l'aide pour obtenir des détails."""

IGNORE_OLDER_THAN = 365

OCCITANIE_PERIMETER_CODE = "76"
OCCITANIE_FINANCER_ID = 91  # "Conseil régional d'Occitanie"


class Command(CrawlerImportCommand):
    """Import data from the Occitanie data feed."""

    SPIDER_CLASS = OccitanieSpider

    def populate_cache(self, *args, **options):
        self.occitanie_perimeter = (
            Perimeter.objects.filter(scale=Perimeter.SCALES.region)
            .filter(code=OCCITANIE_PERIMETER_CODE)
            .get()
        )
        self.occitanie_financer = Backer.objects.get(id=OCCITANIE_FINANCER_ID)

    def line_should_be_processed(self, line):
        """Ignore data older than 1 year.

        Since the data file contains all aids that ever existed on the
        platform, and there is no way to filter it with *active* aids,
        we are forced to rely on a dummy euristic to not import more than 750
        new entries, and ignore all data that was last updated more than one
        year age.

        There is also a "Type" field which only values (AFAIK) can be:
         - Aides
         - Appels à projets
         - Budgets participatifs
        …or empty

        So we filter out lines with an empty `type` field.

        """

        line_type = line["type"]
        date_updated = line["date_updated"]
        now = datetime.now()
        delta = now - date_updated
        return line_type is not None and delta.days < IGNORE_OLDER_THAN

    def extract_import_uniqueid(self, line):
        unique_id = "OCCITANIE_{}".format(line["uniqueid"])
        return unique_id

    def extract_import_data_url(self, line):
        return OPENDATA_URL

    def extract_import_share_licence(self, line):
        return IMPORT_LICENCES.openlicence20

    def extract_name(self, line):
        title = line["title"]
        return title

    def extract_description(self, line):
        description = line["description"]
        return description

    def extract_origin_url(self, line):
        details_url = line["url"]
        return details_url

    def extract_eligibility(self, line):
        return ELIGIBILITY_TXT

    def extract_perimeter(self, line):
        return self.occitanie_perimeter

    def extract_financers(self, line):
        return [self.occitanie_financer]

    # def extract_tags(self, line):
    #     thematique = line['thematique']
    #     tags = thematique.split(', ') if thematique else None
    #     return tags

    def extract_is_call_for_project(self, line):
        type = line["type"]
        if type:
            is_call_for_project = type == "Appels à projets"
        else:
            is_call_for_project = super().extract_is_call_for_project(line)
        return is_call_for_project
