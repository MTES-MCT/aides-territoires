import re
import csv
import logging
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from analytics.utils import get_matomo_stats


DEFAULT_MATOMO_API_METHOD = "Actions.getPageUrls"
DATE_FORMAT = "%Y-%m-%d"  # 2020-12-31
KEYS_CONSIDERED = [
    "label",
    "nb_visits",  # nombre de visiteurs
    "nb_hits",  # nombre de vues
    "url",  # useful for filtering
]
AID_SEARCH_PARAMETERS = ["targeted_audiences", "perimeter", "themes", "categories"]


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Reusable command to fetch/aggregate matomo stats.

    What kind of stats ?
    https://developer.matomo.org/api-reference/reporting-api
    - 'Actions.getPageUrls': views per page URL
    - 'Actions.getPageTitles': views per page title
    - 'Actions.getSiteSearchKeywords': keywords searched in the application

    Why step-by-step with small timeframes instead of 1 single call ?
    - Matomo aggregates results if there are too many, under "<page label> - Others"
    - Therefore we sum keys at each step

    Day incrementation example:
    2020-01-01 --> 2020-01-31 with 3 day increments
    - 2020-01-01 > 2020-01-04
    - 2020-01-05 > 2020-01-08
    ...
    - 2020-01-27 > 2020-01-30
    - 2020-01-31 > 2020-01-31

    Usage:
    pipenv run python manage.py matomo_export_stats
    pipenv run python manage.py matomo_export_stats --api_method Actions.getSiteSearchKeywords
    pipenv run python manage.py matomo_export_stats --custom_segment 'pageUrl=@actioncoeurdeville.aides-territoires.beta.gouv.fr'
    pipenv run python manage.py matomo_export_stats --page_url_prefix_filter 'https://actioncoeurdeville.aides-territoires.beta.gouv.fr/'
    pipenv run python manage.py matomo_export_stats --page_label_prefix_filter '/recherche/formulaire/audience/'
    pipenv run python manage.py matomo_export_stats --page_label_prefix_filter '/aides/?'
    pipenv run python manage.py matomo_export_stats --start_date 2020-05-01
    pipenv run python manage.py matomo_export_stats --start_date 2020-05-01 --end_date 2020-05-31
    pipenv run python manage.py matomo_export_stats --start_date 2020-05-01 --end_date 2020-05-31 --increment_in_days 3
    pipenv run python manage.py matomo_export_stats --start_date 2020-05-01 --end_date 2020-05-31 --increment_in_days 0 (day by day)
    pipenv run python manage.py matomo_export_stats --custom_segment 'pageTitle==Aides-territoires | Recherche' --page_label_prefix_filter '/aides/?' --start_date 2020-05-25 --end_date 2020-12-31 --increment_in_days 0

    TODO:
    - sort csv before export ?
    """  # noqa

    def add_arguments(self, parser):
        parser.add_argument(
            "--api_method",
            type=str,
            default=DEFAULT_MATOMO_API_METHOD,
            help="Specify the Matomo API method. optional.",
        )
        parser.add_argument(
            "--custom_segment",
            type=str,
            default="",
            help="Specify a custom Matomo segment. optional.",
        )
        parser.add_argument(
            "--page_url_prefix_filter",
            type=str,
            default="",
            help="Filter results by a specific page url prefix. optional.",
        )
        parser.add_argument(
            "--page_label_prefix_filter",
            type=str,
            default="",
            help="Filter results by a specific page label prefix. optional.",
        )
        parser.add_argument(
            "--start_date",
            type=str,
            default="2020-01-01",
            help="The range's start date. Use format YYY-MM-DD. optional.",
        )
        parser.add_argument(
            "--end_date",
            type=str,
            default="2020-12-31",
            help="The range's end date. Use format YYY-MM-DD. optional.",
        )
        parser.add_argument(
            "--increment_in_days",
            type=int,
            default=None,
            help="Query the API by increments of X days. 0 = single query. optional.",
        )

    def handle(self, *args, **options):
        # init
        agg_dict_list = []
        agg_label_list = []

        # init date range
        start_datetime = datetime.strptime(options["start_date"], DATE_FORMAT)
        end_datetime = datetime.strptime(options["end_date"], DATE_FORMAT)
        temp_start_datetime = start_datetime
        temp_end_datetime = end_datetime
        if options["increment_in_days"] is not None:
            temp_end_datetime = start_datetime + timedelta(
                days=options["increment_in_days"]
            )

        self.stdout.write("Start date: {}".format(options["start_date"]))
        self.stdout.write("End date: {}".format(options["end_date"]))
        self.stdout.write(
            "Query increment (in days) (None = single query): {}".format(
                str(options["increment_in_days"])
            )
        )

        while temp_start_datetime <= end_datetime:
            # make sure we get all the dates
            if temp_end_datetime > end_datetime:
                temp_end_datetime = end_datetime
            temp_start_date_string = temp_start_datetime.strftime(DATE_FORMAT)
            temp_end_date_string = temp_end_datetime.strftime(DATE_FORMAT)
            self.stdout.write(
                "...querying: {} to {}".format(
                    temp_start_date_string, temp_end_date_string
                )
            )

            data = get_matomo_stats(
                api_method=options["api_method"],
                custom_segment=options["custom_segment"],
                from_date_string=temp_start_date_string,
                to_date_string=temp_end_date_string,
            )

            for page in data:
                # cleanup page dict
                # - keep only specific keys
                # - audiance --> audience
                page = {k: v for k, v in page.items() if k in KEYS_CONSIDERED}
                page["label"] = re.sub(
                    "audiance", "audience", page["label"], flags=re.IGNORECASE
                )

                if page["label"].startswith(
                    options["page_label_prefix_filter"]
                ) and page.get("url", "").startswith(options["page_url_prefix_filter"]):
                    # notify if there are aggregated labels
                    if "Others" in page["label"]:
                        self.stdout.write(page["label"])

                    # sum existing label data
                    if page["label"] in agg_label_list:
                        for index, item in enumerate(agg_dict_list):
                            if item["label"] == page["label"]:
                                for key in item.keys():
                                    if isinstance(item[key], int) and (key in page):
                                        agg_dict_list[index][key] += int(page[key])
                    # add new label data
                    else:
                        agg_label_list.append(page["label"])
                        agg_dict_list.append(page)

            # increment dates
            if options["increment_in_days"] is not None:
                temp_start_datetime = temp_start_datetime + timedelta(
                    days=options["increment_in_days"] + 1
                )
                temp_end_datetime = temp_end_datetime + timedelta(
                    days=options["increment_in_days"] + 1
                )
            else:
                break

        # write dict to csv
        if len(agg_dict_list):
            keys = agg_dict_list[0].keys()
            filename = f"matomo_{slugify(options['api_method'])}_{options['start_date']}_{options['end_date']}.csv"  # noqa
            with open(filename, "w", newline="") as output_file:
                dict_writer = csv.DictWriter(
                    output_file, fieldnames=keys, extrasaction="ignore"
                )
                dict_writer.writeheader()
                dict_writer.writerows(agg_dict_list)
                self.stdout.write(
                    self.style.SUCCESS("File created: {}".format(filename))
                )
        else:
            self.stdout.write("Returned no results")
