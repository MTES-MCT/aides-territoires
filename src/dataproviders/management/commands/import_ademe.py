import os
import re
from datetime import datetime
from xml.etree import ElementTree
from html import unescape
from unicodedata import normalize
from bs4 import BeautifulSoup as bs

from django.core.management.base import BaseCommand

from geofr.models import Perimeter
from aids.models import Aid


FEED_URI = 'https://appelsaprojets-bo.ademe.fr/App_services/DMA/xml_appels_projets.ashx?tlp=1'  # noqa
BACKER_ID = 22
ADMIN_ID = 1

# Convert Ademe's `cible` value to our value
AUDIANCES_DICT = {
    'Entreprises et Monde Agricole': [Aid.AUDIANCES.private_sector],
    'Recherche et Innovation': [Aid.AUDIANCES.researcher],
    'Collectivités et Secteur public': [
        Aid.AUDIANCES.commune,
        Aid.AUDIANCES.department,
        Aid.AUDIANCES.region,
        Aid.AUDIANCES.epci,
    ],
    'Tout Public': [
        Aid.AUDIANCES.commune,
        Aid.AUDIANCES.department,
        Aid.AUDIANCES.region,
        Aid.AUDIANCES.epci,
        Aid.AUDIANCES.lessor,
        Aid.AUDIANCES.association,
        Aid.AUDIANCES.private_person,
        Aid.AUDIANCES.researcher,
        Aid.AUDIANCES.private_sector,
    ]
}


class Command(BaseCommand):
    """Import data from the Ademe data feed."""

    def add_arguments(self, parser):
        parser.add_argument('data-file', nargs=1, type=str)

    def handle(self, *args, **options):
        new_aids = []
        self.france = Perimeter.objects.get(code='FRA')

        data_file = os.path.abspath(options['data-file'][0])
        xml_tree = ElementTree.parse(data_file)
        xml_root = xml_tree.getroot()
        for xml_elt in xml_root:
            if xml_elt.tag == 'appel':
                aid = self.create_aid(xml_elt)
                if aid is not None:
                    new_aids.append(aid)

        Aid.objects.bulk_create(new_aids)
        AidBacker = Aid._meta.get_field('backers').remote_field.through
        aid_backers = []
        for aid in new_aids:
            aid_backers.append(AidBacker(
                aid=aid,
                backer_id=BACKER_ID))
        AidBacker.objects.bulk_create(aid_backers)

    def create_aid(self, xml):
        closed = xml.find('appel_cloture').text
        if closed == '1':
            return None

        data_id = xml.attrib['id']
        unique_id = 'ADEME_{}'.format(data_id)
        title = xml.find('.//titre').text
        perimeter = xml.find('.//couverture_geographique').text  # noqa
        description = self.clean_description(xml.find('presentation').text)

        publication_date_text = xml.find('.//date_publication').text
        publication_date = datetime.strptime(
            publication_date_text,
            '%d/%m/%Y %H:%M:%S')
        closure_date_text = xml.find('.//date_cloture').text
        closure_date = datetime.strptime(
            closure_date_text,
            '%d/%m/%Y').date()

        details_url = xml.find('.//lien_page_edition').text
        clean_url = details_url.replace(' ', '%20')

        targets = self.extract_targets(xml)

        aid = Aid(
            name=title,
            author_id=ADMIN_ID,
            description=description,
            eligibility='',
            perimeter=self.france,
            url=clean_url,
            start_date=publication_date,
            submission_deadline=closure_date,
            targeted_audiances=targets,
            is_imported=True,
            import_uniqueid=unique_id,
        )
        aid.set_slug()
        aid.set_search_vector()
        return aid

    def clean_description(self, raw_description):
        unescaped = unescape(raw_description or '')
        unstyled = re.sub(' style="[^"]+"', '', unescaped)
        unquoted = unstyled \
            .replace('“', '"') \
            .replace('”', '"') \
            .replace('’', "'")
        normalized = normalize('NFKC', unquoted)
        soup = bs(normalized)
        prettified = soup.prettify()
        return prettified

    def extract_targets(self, xml):
        targets = []
        target_elts = xml.findall('.//cibles/cible')
        for element in target_elts:
            ademe_target = element.text
            our_targets = AUDIANCES_DICT[ademe_target]
            targets += our_targets
        return list(set(targets))
