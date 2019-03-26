import scrapy
from dataproviders.utils import content_prettify


# This is a reference specific to the grandest.fr site.
# When you click on the filter form "filtrer par bénéficiaires" field and
# choose "collectivités", you get a new parameter ?beneficiaire=63 in the url.
EPCI_AUDIANCE_CODE = '63'


class GrandEstSpider(scrapy.Spider):
    name = 'grand_est'

    BASE_URL = 'https://www.grandest.fr/'
    start_urls = [
        'https://www.grandest.fr/aides/?beneficiaire={}'.format(
            EPCI_AUDIANCE_CODE),
    ]

    def parse(self, response):
        links = response.css('a.card::attr("href")').getall()
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.aid_parse)

        # The web site pagination is completely broken without javascript
        # so we have to pass a weird combination of paramaters to the url
        next = response.css('a[rel=next]::attr("href")').get()
        if next:
            page_number = next.split('/')[-2]
            real_next_url = '{base_url}page/{page}/?beneficiaire={beneficiaire}&pg={page}'.format(  # noqa
                base_url=self.start_urls[0],
                beneficiaire=EPCI_AUDIANCE_CODE,
                page=page_number)
            yield scrapy.Request(real_next_url, callback=self.parse)

    def aid_parse(self, response):
        title = response.xpath('//meta[@property="og:title"]/@content').get()
        description = response.css('div.pf-content').get()
        contact = response.css('div.know').get()

        current_url = response.request.url
        unique_id = current_url.split('/')[-2]

        yield {
            'title': content_prettify(title),
            'description': content_prettify(description),
            'current_url': current_url,
            'uniqueid': unique_id,
            'contact': content_prettify(contact),
        }
