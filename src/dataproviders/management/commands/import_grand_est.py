import scrapy
from scrapy.crawler import CrawlerProcess

from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid
from dataproviders.management.commands.base import BaseImportCommand
from dataproviders.scrapers.grand_est import GrandEstSpider

ADMIN_ID = 1

GRAND_EST_CODE = '44'


ELIGIBILITY_TXT = '''Rendez-vous sur le site de la région Grand-Est pour
obtenir les informations relatives aux conditions d'éligibilité.
'''


class Command(BaseImportCommand):
    """Import data from the eaurmc.fr site."""

    def populate_cache(self, *args, **options):
        self.perimeter = Perimeter.objects \
            .filter(scale=Perimeter.TYPES.region) \
            .filter(code=GRAND_EST_CODE) \
            .get()

        self.backer = Backer.objects.get(
            name="Région Grand Est")

    def fetch_data(self, **options):
        results = []
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'LOG_LEVEL': 'INFO',
        })
        process.crawl(GrandEstSpider)

        def add_to_results(item, response, spider):
            results.append(item)

        for p in process.crawlers:
            p.signals.connect(
                add_to_results, signal=scrapy.signals.item_scraped)
        process.start()

        for result in results:
            yield result

    def extract_author_id(self, line):
        return ADMIN_ID

    def extract_import_uniqueid(self, line):
        return 'GE_{}'.format(line['uniqueid'])

    def extract_import_data_url(self, line):
        return line['current_url']

    def extract_import_share_licence(self, line):
        return Aid.IMPORT_LICENCES.unknown

    def extract_name(self, line):
        return line['title']

    def extract_description(self, line):
        return line['description']

    def extract_eligibility(self, line):
        return ELIGIBILITY_TXT

    def extract_perimeter(self, line):
        return self.perimeter

    def extract_backers(self, line):
        return [self.backer]

    def extract_contact_detail(self, line):
        return line['contact']
