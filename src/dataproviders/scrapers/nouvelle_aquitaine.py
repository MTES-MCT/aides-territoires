# flake8: noqa
import scrapy
from xml.etree import ElementTree

from dataproviders.utils import content_prettify


class NouvelleAquitaineSpider(scrapy.Spider):
    name = 'nouvelle_aquitaine'

    start_urls = [
        'https://les-aides.nouvelle-aquitaine.fr/fiches-rss.xml'
    ]

    def parse(self, response):
        xml_root = ElementTree.fromstring(response.text)
        for xml_elt in xml_root.find('channel'):
            if xml_elt.tag == 'item':
                for key in xml_elt:
                    if key.tag == 'guid':
                        request = scrapy.Request(key.text, callback=self.aid_parse)
                    elif key.tag == 'pubDate':
                        request.meta['pub_date'] = key.text
                yield request

    def aid_parse(self, response):
        title = response.css('h1.headline-aide::text').get().strip()
        subtitle = response.css('div.mod-chapo').get().strip()

        categorie = response.css('ul.m-breadcrumb__list > li:nth-child(2) > span::text').get()

        is_call_for_project = False
        if response.css('span.tag-appel-projet').get() or response.css('span.tag-appel-manifestation').get():
            is_call_for_project = True
        is_dispositif_europe = False
        if response.css('span.tag-europe').get():
            is_dispositif_europe = True

        aid_header = {
            'publics_concernes': '',  # targeted_audiences
            'domaines_secondaires': '',  # categories
            'date_de_fin_de_publication': ''  # submission_deadline
        }
        for index, item in enumerate(response.css('div.categories')):
            aid_header_key = list(aid_header.keys())[index]
            aid_header[aid_header_key] = content_prettify(item.css('p::text').get()).strip().replace('\n', '').replace('   ', '').replace('  ,  ', ';')

        aid_details = {
            'objectifs': '',
            'calendrier': '',
            'beneficiaires': '',
            'montant': '',
            'criteres': '',
            'modalites': '',
            # 'documents': '',
            # 'contact': ''
        }
        for index, item in enumerate(response.css('div.dispositif-aide > div.mod-textSimple')):
            aid_details_key = list(aid_details.keys())[index]
            aid_details[aid_details_key] = content_prettify(item.get())

        contact = response.css('div.mod-contactAddress').get()

        documents = response.css('div.mod-listDownload').get()

        current_url = response.request.url

        yield {
            'title': title,
            'description': subtitle + '<br />' + content_prettify(aid_details['objectifs']),
            'categorie': categorie,
            'is_call_for_project': is_call_for_project,
            'is_dispositif_europe': is_dispositif_europe,
            **aid_header,
            **aid_details,
            'contact': content_prettify(contact),
            'documents': content_prettify(documents),
            'pub_date': response.meta['pub_date'],
            'current_url': current_url,
        }
