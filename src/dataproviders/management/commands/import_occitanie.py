from dataproviders.management.commands.base import CrawlerImportCommand
from dataproviders.scrapers.occitanie import OccitanieSpider
from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid


OPENDATA_URL = 'https://data.laregion.fr/explore/dataset/aides-et-appels-a-projets-de-la-region-occitanie/information/'  # noqa


ELIGIBILITY_TXT = '''Consultez la page de l'aide pour obtenir des détails.'''


class Command(CrawlerImportCommand):
    """Import data from the Ademe data feed."""

    SPIDER_CLASS = OccitanieSpider

    def populate_cache(self, *args, **options):
        self.occitanie_perimeter = Perimeter.objects \
            .filter(scale=Perimeter.TYPES.region) \
            .filter(code='76') \
            .get()
        self.occitanie_backer = Backer.objects.get(name='Région Occitanie')

    def line_should_be_processed(self, line):
        return True

    def extract_import_uniqueid(self, line):
        unique_id = 'OCCITANIE_{}'.format(line['uniqueid'])
        return unique_id

    def extract_import_data_url(self, line):
        return OPENDATA_URL

    def extract_import_share_licence(self, line):
        return Aid.IMPORT_LICENCES.openlicence20

    def extract_name(self, line):
        title = line['title']
        return title

    def extract_description(self, line):
        description = line['description']
        return description

    def extract_origin_url(self, line):
        details_url = line['url']
        return details_url

    def extract_eligibility(self, line):
        return ELIGIBILITY_TXT

    def extract_perimeter(self, line):
        return self.occitanie_perimeter

    def extract_backers(self, line):
        return [self.occitanie_backer]

    def extract_tags(self, line):
        thematique = line['thematique']
        tags = thematique.split(', ') if thematique else None
        return tags

    def extract_is_call_for_project(self, line):
        type = line['type']
        if type:
            is_call_for_project = type == 'Appels à projets'
        else:
            is_call_for_project = super().extract_is_call_for_project(line)
        return is_call_for_project
