# flake8: noqa
import re
import csv
import logging
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from analytics.utils import get_matomo_page_urls_stats


DATE_FORMAT = '%Y-%m-%d'  # 2020-12-31
KEYS_CONSIDERED = [
    'label',
    'nb_visits',  # nombre de visiteurs
    'nb_hits'  # nombre de vues
]
AID_SEARCH_PARAMETERS = [
    'targeted_audiences',
    'perimeter',
    'themes',
    'categories'
]


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Reusable command to fetch/aggregate matomo page view stats.

    Why step-by-step with small timeframes instead of 1 single call ?
    - Matomo aggregates results if there are too many, under "<page label> - Others"
    - Therefore we sum keys at each step

    Day incrementation example :
    2020-01-01 --> 2020-01-31 with 3 day increments
    - 2020-01-01 > 2020-01-04
    - 2020-01-05 > 2020-01-08
    ...
    - 2020-01-27 > 2020-01-30
    - 2020-01-31 > 2020-01-31

    Usage :
    pipenv run python manage.py matomo_export_getpageurls
    pipenv run python manage.py matomo_export_getpageurls --page_label_prefix_filter '/recherche/formulaire/audience/'
    pipenv run python manage.py matomo_export_getpageurls --page_label_prefix_filter '/aides/?'
    pipenv run python manage.py matomo_export_getpageurls --start_date 2020-05-01
    pipenv run python manage.py matomo_export_getpageurls --start_date 2020-05-01 --end_date 2020-05-31
    pipenv run python manage.py matomo_export_getpageurls --start_date 2020-05-01 --end_date 2020-05-31 --increment_in_days 3
    pipenv run python manage.py matomo_export_getpageurls --start_date 2020-05-01 --end_date 2020-05-31 --increment_in_days 0 (day by day)
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--page_label_prefix_filter', type=str,
            default="",
            help="filter results by a specific page label prefix. optional."
        )
        parser.add_argument(
            '--start_date', type=str,
            default="2020-01-01",
            help="the range's start date. Use format YYY-MM-DD. optional."
        )
        parser.add_argument(
            '--end_date', type=str,
            default="2020-12-31",
            help="the range's end date. Use format YYY-MM-DD. optional."
        )
        parser.add_argument(
            '--increment_in_days', type=int,
            default=None,
            help="query the API by increments of X days. 0 = single query. optional."
        )

    def handle(self, *args, **options):
        # init
        agg_dict_list = []
        agg_label_list = []

        # init date range
        start_datetime = datetime.strptime(options['start_date'], DATE_FORMAT)
        end_datetime = datetime.strptime(options['end_date'], DATE_FORMAT)
        temp_start_datetime = start_datetime
        temp_end_datetime = end_datetime
        if options['increment_in_days'] is not None:
            temp_end_datetime = start_datetime + timedelta(days=options['increment_in_days'])

        self.stdout.write('Start date: {}'.format(options['start_date']))
        self.stdout.write('End date: {}'.format(options['end_date']))
        self.stdout.write('Query increment (in days) (None = single query): {}'.format(str(options['increment_in_days'])))

        while (temp_start_datetime <= end_datetime):
            # make sure we get all the dates
            if temp_end_datetime > end_datetime:
                temp_end_datetime = end_datetime
            temp_start_date_string = temp_start_datetime.strftime(DATE_FORMAT)
            temp_end_date_string = temp_end_datetime.strftime(DATE_FORMAT)
            self.stdout.write('...querying: {} to {}'.format(temp_start_date_string, temp_end_date_string))

            data = get_matomo_page_urls_stats(
                from_date_string=temp_start_date_string,
                to_date_string=temp_end_date_string)

            for page in data:
                # cleanup page dict
                # - keep only specific keys
                # - audiance --> audience
                page = {k: v for k, v in page.items() if k in KEYS_CONSIDERED}
                page['label'] = re.sub("audiance", "audience", page['label'], flags=re.IGNORECASE)

                # process audience pages
                if page['label'].startswith(options['page_label_prefix_filter']):
                    # notify if there are aggregated labels
                    if " - Others" in page['label']:
                        self.stdout.write(page['label'])

                    # sum existing label data
                    if page['label'] in agg_label_list:
                        for index, item in enumerate(agg_dict_list):
                            if item['label'] == page['label']:
                                for key in item.keys():
                                    if (type(item[key]) == int) and (key in page):
                                        agg_dict_list[index][key] += int(page[key])
                    # add new label data
                    else:
                        agg_label_list.append(page['label'])
                        agg_dict_list.append(page)

            # increment dates
            if options['increment_in_days'] is not None:
                temp_start_datetime = temp_start_datetime + timedelta(days=options['increment_in_days']+1)
                temp_end_datetime = temp_end_datetime + timedelta(days=options['increment_in_days']+1)
            else:
                break

        # write dict to csv
        keys = agg_dict_list[0].keys()
        filename = f"matomo_getpageurls_{slugify(options['page_label_prefix_filter'])}_{options['start_date']}_{options['end_date']}.csv"
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
            dict_writer.writeheader()
            dict_writer.writerows(agg_dict_list)
            self.stdout.write(self.style.SUCCESS('File created: {}'.format(filename)))
