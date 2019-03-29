import json
import scrapy
from dataproviders.utils import content_prettify
from bs4 import BeautifulSoup as bs


def custom_prettify(raw_text):
    """Prettify content and performs some specific cleaning tasks."""
    soup = bs(raw_text, features='html.parser')
    download_box = soup.select('div.boite_telechargements_libre')
    for box in download_box:
        box.decompose()

    return content_prettify(soup.prettify())


class OccitanieSpider(scrapy.Spider):
    name = 'occitanie'

    BASE_URL = 'https://www.laregion.fr/'
    start_urls = [
        'https://data.laregion.fr/explore/dataset/aides-et-appels-a-projets-de-la-region-occitanie/download/?format=json&timezone=Europe/Berlin',  # noqa
    ]

    def parse(self, response):
        json_data = json.loads(response.body_as_unicode())
        for data in json_data:
            request = scrapy.Request(
                data['fields']['url'], callback=self.aid_parse)
            request.meta['uniqueid'] = data['recordid']
            request.meta['fields'] = data['fields']
            yield request

    def aid_parse(self, response):
        title = response.css('h1.main-content__title::text').get()
        description = response.css('div.main-content__texte').get()
        fields = response.meta['fields']

        yield {
            'title': content_prettify(title),
            'description': custom_prettify(description),
            'url': fields['url'],
            'uniqueid': response.meta['uniqueid'],
            'thematique': fields.get('thematique', None),
            'type': fields.get('type', None),
        }
