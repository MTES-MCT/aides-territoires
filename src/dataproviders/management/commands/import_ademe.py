import os
import re
from datetime import datetime
from xml.etree import ElementTree
from xml.dom import minidom
from html import unescape
from unicodedata import normalize
from bs4 import BeautifulSoup as bs

from django.core.management.base import BaseCommand

from aids.models import Aid


FEED_URI = 'https://appelsaprojets-bo.ademe.fr/App_services/DMA/xml_appels_projets.ashx?tlp=1'


class Command(BaseCommand):
    """Import data from the Ademe data feed."""

    def add_arguments(self, parser):
        parser.add_argument('data-file', nargs=1, type=str)

    def handle(self, *args, **options):
        data_file = os.path.abspath(options['data-file'][0])
        xml_tree = ElementTree.parse(data_file)
        xml_root = xml_tree.getroot()
        for xml_elt in xml_root:
            if xml_elt.tag   == 'appel':
                self.import_aid(xml_elt)

    def import_aid(self, xml):
        data_id = xml.attrib['id']
        unique_id = 'ADEME_{}'.format(data_id)
        title = xml.find('.//titre').text
        perimeter = xml.find('.//couverture_geographique').text
        details_url = xml.find('.//lien_page_edition').text
        description = self.clean_description(xml.find('presentation').text)
        publication_date_text = xml.find('.//date_publication').text
        publication_date = datetime.strptime(
            publication_date_text,
            '%d/%m/%Y %H:%M:%S')
        closure_date_text = xml.find('.//date_cloture').text
        closure_date = datetime.strptime(
            closure_date_text,
            '%d/%m/%Y').date()
        print(title)

    def clean_description(self, raw_description):
        unescaped = unescape(raw_description)
        unstyled = re.sub(' style="[^"]+"', '', unescaped)
        unquoted = unstyled \
            .replace('“', '"') \
            .replace('”', '"') \
            .replace('’', "'")
        normalized = normalize('NFKC', unquoted)
        soup = bs(normalized)
        prettified = soup.prettify()
        return prettified
