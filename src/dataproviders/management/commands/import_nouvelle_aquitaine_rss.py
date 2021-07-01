# flake8: noqa
import os
import csv
import locale
import hashlib
from datetime import datetime

from django.utils import timezone

from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.management.commands.base import CrawlerImportCommand
from dataproviders.scrapers.nouvelle_aquitaine import NouvelleAquitaineSpider
from geofr.models import Perimeter
from backers.models import Backer
from categories.models import Category
from aids.models import Aid


DATA_SOURCE = DataSource.objects \
    .prefetch_related('perimeter', 'backer') \
    .get(pk=1)

AUDIENCES_DICT = {}
AUDIENCES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/nouvelle_aquitaine_rss_audiences_mapping.csv'
SOURCE_COLUMN_NAME = 'Bénéficiaires Nouvelle-Aquitaine'
AT_COLUMN_NAMES = ['Bénéficiaires AT 1', 'Bénéficiaires AT 2', 'Bénéficiaires AT 3', 'Bénéficiaires AT 4']
with open(AUDIENCES_MAPPING_CSV_PATH) as csv_file:
    csvreader = csv.DictReader(csv_file, delimiter=",")
    for index, row in enumerate(csvreader):
        if row[AT_COLUMN_NAMES[0]]:
            AUDIENCES_DICT[row[SOURCE_COLUMN_NAME]] = []
            for column in AT_COLUMN_NAMES:
                if row[column]:
                    audience = next(choice[0] for choice in Aid.AUDIENCES if choice[1] == row[column])
                    AUDIENCES_DICT[row[SOURCE_COLUMN_NAME]].append(audience)

CATEGORIES_DICT = {}
CATEGORIES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/nouvelle_aquitaine_rss_categories_mapping.csv'
SOURCE_COLUMN_NAME = 'Thématique Nouvelle-Aquitaine'
AT_COLUMN_NAMES = ['Sous-thématique AT 1', 'Sous-thématique AT 2', 'Sous-thématique AT 3']
with open(CATEGORIES_MAPPING_CSV_PATH) as csv_file:
    csvreader = csv.DictReader(csv_file, delimiter=",")
    for index, row in enumerate(csvreader):
        if row[AT_COLUMN_NAMES[0]]:
            CATEGORIES_DICT[row[SOURCE_COLUMN_NAME]] = []
            for column in AT_COLUMN_NAMES:
                if row[column]:
                    category = Category.objects.get(name=row[column])
                    CATEGORIES_DICT[row[SOURCE_COLUMN_NAME]].append(category)

ELIGIBILITY_TXT = '''Consultez la page de l'aide pour obtenir des détails.'''

XML_ITEM_EXAMPLE = """
<item>
    <title>Développement d'une offre locative à destination des jeunes agriculteurs</title>
    <description>Cet appel à projet a pour objectif de faciliter l’installation des nouveaux arrivants et jeunes agriculteurs.trices âgé.e.s de 18 à 40 ans, qui envisagent de développer une activité professionnelle agricole dans un territoire rural.Il s’agit d’accompagner les initiatives facilitant l’installation des jeunes agriculteurs.trices sous forme de logements passerelles.&#13;</description>
    <guid isPermaLink="true">https://les-aides.nouvelle-aquitaine.fr/amenagement-du-territoire/developpement-dune-offre-locative-destination-des-jeunes-agriculteurs</guid>
    <pubDate>Sat, 21 Dec 19 11:00:28 +0100</pubDate>
    <source url="https://les-aides.nouvelle-aquitaine.fr/amenagement-du-territoire/developpement-dune-offre-locative-destination-des-jeunes-agriculteurs">Développement d'une offre locative à destination des jeunes agriculteurs</source>
    <category>Appel à projet, Collectivité territoriale, GIE - Groupement d'intérêt économique, Association, Établissement public, Entreprise, Logement</category>
</item>
"""


class Command(CrawlerImportCommand):
    """
    Import data from the Nouvelle Aquitaine RSS feed.

    Strategy:
    - the data comes from an RSS feed, XML-formated
    - we first loop on every xml item
    - then crawl the aid url using Scrapy
    
    Comments:
    - <title> content equals <source> content
    - <guid>: contains the link to the aid HTML
    """

    SPIDER_CLASS = NouvelleAquitaineSpider

    def handle(self, *args, **options):
        DATA_SOURCE.date_last_access = timezone.now()
        DATA_SOURCE.save()
        super().handle(*args, **options)

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        url_md5_hash = hashlib.md5(
            line['current_url'].encode('utf-8')).hexdigest()
        unique_id = 'NOUVELLE_AQUITAINE_{}'.format(url_md5_hash)
        return unique_id

    def extract_import_data_url(self, line):
        return DATA_SOURCE.import_data_url

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_name(self, line):
        title = line['title'][:180]
        return title

    def extract_description(self, line):
        description = line['description']
        if line['objectifs']:
            description += '<strong>{}</strong>: {}<br /><br />'.format('Objectifs', line['objectifs'])
        return description

    def extract_origin_url(self, line):
        origin_url = line['current_url']
        return origin_url

    def extract_eligibility(self, line):
        eligibility = ''
        metadata = {
            'calendrier': 'Calendrier',
            'beneficiaires': 'Bénéficiaires',
            'criteres': 'Critères de sélection',
            'modalites': 'Comment faire ma demande ?',
        }
        for elem in metadata:
            if line[elem]:
                eligibility += '<strong>{}</strong>: {}<br /><br />'.format(metadata[elem], line[elem])
        return eligibility

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_contact(self, line):
        return line['contact']

    def extract_is_call_for_project(self, line):
        return line['is_call_for_project']

    def extract_date_published(self, line):
        """Example: Thu, 19 Dec 19 13:49:51 +0100"""
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        date_published_format = '%a, %d %b %y %H:%M:%S %z'
        date_published = datetime.strptime(line['pub_date'], date_published_format)
        return date_published

    def extract_submission_deadline(self, line):
        if line['date_de_fin_de_publication']:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
            submission_deadline_format = '%d %B %Y'
            submission_deadline = datetime.strptime(line['date_de_fin_de_publication'], submission_deadline_format)
            return submission_deadline
        return None

    def extract_categories(self, line):
        """
        Exemple of string to process: "Performance et compétitivité;Agroalimentaire"
        Split the string, loop on the values and match to our Categories
        """
        categories = line.get('domaines_secondaires', '').split(';')
        aid_categories = []
        for category in categories:
            if category in CATEGORIES_DICT:
                aid_categories.extend(CATEGORIES_DICT.get(category, []))
            else:
                self.stdout.write(self.style.ERROR(f'Category {category} not mapped'))
        return aid_categories

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process: "Association;Collectivité territoriale;Entreprise;Établissement public"
        Split the string, loop on the values and match to our Audiences
        """
        audiences = line.get('publics_concernes', '').split(';')
        aid_audiences = []
        for audience in audiences:
            if audience in AUDIENCES_DICT:
                aid_audiences.extend(AUDIENCES_DICT.get(audience, []))
            else:
                self.stdout.write(self.style.ERROR(f'Audience {audience} not mapped'))
        return aid_audiences

    def extract_project_examples(self, line):
        """Use the project_examples textfield to store metadata"""
        content = ''
        metadata = {
            'categorie': 'Thématique',
            # 'domaines_secondaires': 'Domaines secondaires',
            'is_dispositif_europe': 'Dispositif de l\'UE',
            # 'objectifs': 'Objectifs',
            # 'pub_date': 'Date de publication'
        }
        for elem in metadata:
            if line[elem]:
                content += '<strong>{}</strong>: {}<br /><br />'.format(metadata[elem], line[elem])
        return content
