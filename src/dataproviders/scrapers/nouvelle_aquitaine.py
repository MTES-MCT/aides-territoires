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
        title = response.css('h1.headline-aide::text').get()
        description = response.css(
            'div.container > div.chapo > div._layout > div.link-wrapper').get()
        categorie = response.xpath('//li[@itemprop="itemListElement"]//span[@itemprop="name"]/text()')[1].get()

        is_call_for_project = False
        if response.css('span.tag-appel-projet').get() or response.css('span.tag-appel-manifestation').get():
            is_call_for_project = True
        is_dispositif_europe = False
        if response.css('span.tag-europe').get():
            is_dispositif_europe = True

        aid_header = {
            'publics_concernes': '',  # targeted_audiences
            'domaines_secondaires': '',
            'date_de_fin_de_publication': ''  # submission_deadline
        }
        for index, item in enumerate(response.css('div.categories')):
            aid_header_key = list(aid_header.keys())[index]
            aid_header[aid_header_key] = content_prettify(item.css('p::text').get()).strip().replace('\n', '').replace('   ', '')

        aid_details = {
            'echeances': '',
            'objectifs': '',
            'beneficiaires': '',
            'modalites': ''
        }
        for index, item in enumerate(response.css('section.dispositif-aide > div.container > div.texte-simple > div._layout')):
            aid_details_key = list(aid_details.keys())[index]
            aid_details[aid_details_key] = content_prettify(item.get())

        contact = response.css('div.contact-adresses').get()

        current_url = response.request.url

        yield {
            'title': title,
            'description': content_prettify(description),
            'categorie': categorie,
            'is_call_for_project': is_call_for_project,
            'is_dispositif_europe': is_dispositif_europe,
            **aid_header,
            **aid_details,
            'contact': content_prettify(contact),
            'pub_date': response.meta['pub_date'],
            'current_url': current_url,
        }
