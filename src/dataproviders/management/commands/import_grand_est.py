from geofr.models import Perimeter
from backers.models import Backer
from aids.models import Aid
from dataproviders.management.commands.base import CrawlerImportCommand
from dataproviders.scrapers.grand_est import GrandEstSpider

ADMIN_ID = 1

GRAND_EST_CODE = '44'


ELIGIBILITY_TXT = '''Rendez-vous sur le site de la région Grand-Est pour
obtenir les informations relatives aux conditions d'éligibilité.
'''


class Command(CrawlerImportCommand):
    """Import data from the eaurmc.fr site."""

    SPIDER_CLASS = GrandEstSpider

    def populate_cache(self, *args, **options):
        self.perimeter = Perimeter.objects \
            .filter(scale=Perimeter.TYPES.region) \
            .filter(code=GRAND_EST_CODE) \
            .get()

        self.backer = Backer.objects.get(
            name="Région Grand Est")

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

    def extract_is_call_for_project(self, line):
        return line['is_call_for_project']

    def extract_tags(self, line):
        return line['category'].split(' - ') if line['category'] else []

    def extract_submission_deadline(self, line):
        return line['submission_deadline'] or None

    def extract_targeted_audiances(self, line):
        return [Aid.AUDIANCES.epci]
