# flake8: noqa
import os
import requests
import xmltodict
from datetime import datetime
from xml.etree import ElementTree

from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify, build_audiences_mapping_dict
from dataproviders.management.commands.base import BaseImportCommand
from geofr.models import Perimeter


ADMIN_ID = 1

DATA_SOURCE = DataSource.objects \
    .prefetch_related('perimeter', 'backer') \
    .get(pk=5)

AUDIENCES_MAPPING_CSV_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/ademe_audiences_mapping.csv'
AUDIENCES_DICT = build_audiences_mapping_dict(
    AUDIENCES_MAPPING_CSV_PATH,
    source_column_name='Bénéficiaires ADEME',
    at_column_names=['Bénéficiaires AT 1', 'Bénéficiaires AT 2', 'Bénéficiaires AT 3', 'Bénéficiaires AT 4', 'Bénéficiaires AT 5', 'Bénéficiaires AT 6', 'Bénéficiaires AT 7', 'Bénéficiaires AT 8', 'Bénéficiaires AT 9'])

ELIGIBILITY_TXT = '''
Il est vivement conseillé de contacter l'ADEME en amont du dépôt du dossier
pour tous renseignements ou conseils relatifs au montage et à la soumission
de votre dossier.
'''

ADEME_URL = 'https://www.ademe.fr/'


class Command(BaseImportCommand):
    """Import data from the Ademe data feed."""

    def add_arguments(self, parser):
        parser.add_argument('data-file', nargs='?', type=str)

    def fetch_data(self, **options):
        # If no file was passed as a parameter, download the original xml file
        # on Ademe's website
        if options['data-file']:
            data_file = os.path.abspath(options['data-file'])
            xml_tree = ElementTree.parse(data_file)
            xml_root = xml_tree.getroot()
        else:
            req = requests.get(DATA_SOURCE.import_api_url)
            xml_root = ElementTree.fromstring(req.text)

        for xml_elt in xml_root:
            if xml_elt.tag == 'appel':
                yield xml_elt

    def handle(self, *args, **options):
        self.france = Perimeter.objects.get(code='FRA')
        regions_qs = Perimeter.objects \
            .filter(scale=Perimeter.SCALES.region)
        self.regions = list(regions_qs)
        super().handle(*args, **options)

    def line_should_be_processed(self, line):
        """Ignore line with expired aids."""
        closed = line.find('appel_cloture').text
        return closed != '1'

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        data_id = line.attrib['id']
        unique_id = 'ADEME_{}'.format(data_id)
        return unique_id

    def extract_import_data_url(self, line):
        return DATA_SOURCE.import_data_url

    def extract_import_share_licence(self, line):
        return IMPORT_LICENCES.unknown

    def extract_import_raw_object(self, line):
        line_string = ElementTree.tostring(line, encoding='unicode')
        return xmltodict.parse(line_string)

    def extract_author_id(self, line):
        return ADMIN_ID

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_name(self, line):
        title = line.find('.//titre').text
        return title[:180]

    def extract_description(self, line):
        description = content_prettify(line.find('presentation').text)
        return description

    def extract_start_date(self, line):
        publication_date_text = line.find('.//date_publication').text
        publication_date = datetime.strptime(
            publication_date_text,
            '%d/%m/%Y %H:%M:%S')
        return publication_date

    def extract_submission_deadline(self, line):
        closure_date_text = line.find('.//date_cloture').text
        closure_date = datetime.strptime(
            closure_date_text,
            '%d/%m/%Y').date()
        return closure_date

    def extract_origin_url(self, line):
        details_url = line.find('.//lien_page_edition').text
        clean_url = details_url.replace(' ', '%20')
        return clean_url

    def extract_eligibility(self, line):
        return ELIGIBILITY_TXT

    def extract_targeted_audiences(self, line):
        targets = []
        target_elts = line.findall('.//cibles/cible')
        print(target_elts)
        for element in target_elts:
            ademe_target = element.text
            our_targets = AUDIENCES_DICT[ademe_target]
            targets += our_targets
        print(list(set(targets)))
        return list(set(targets))

    def extract_perimeter(self, line):
        """Extract the perimeter value.

        In the Ademe feed, there is one xml tag `<couverture_geographique/>`
        with two values: `Nationale` or `Régionale`.

        When the perimeter is regional, the actual region is not given.
        Our only way to extract it is to find the region name in the title
        if we are lucky.
        """
        chars_to_replace = {
            'é': 'e',
            'è': 'e',
            'î': 'i',
            '-': ' '
        }
        perimeter_choice = line.find('.//couverture_geographique').text
        aid_title = line.find('.//titre').text.lower()
        for old_char, new_char in chars_to_replace.items():
            aid_title = aid_title.replace(old_char, new_char)

        perimeter = None
        if perimeter_choice == 'Nationale':
            perimeter = self.france
        else:
            # This is a nasty hack
            # Test all region names and see if they appear in the title
            for region in self.regions:

                # We remove all special chars from region name and aid title
                # in a futile atempt to increase our match rate.
                region_name = region.name.lower()
                for old_char, new_char in chars_to_replace.items():
                    region_name = region_name.replace(old_char, new_char)

                if region_name in aid_title:
                    perimeter = region
                    break

            if perimeter is None:
                perimeter = self.france

        return perimeter
