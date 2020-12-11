import requests

from django.conf import settings
from django.utils import timezone

from functools import lru_cache

from stats.models import Event


def log_event(category, event, meta='', value=None):
    Event.objects.create(
        category=category,
        event=event,
        meta=meta,
        value=value)


@lru_cache()
def get_matomo_stats_from_page_title(page_title, from_date_string, to_date_string=timezone.now().strftime('%Y-%m-%d')):  # noqa
    """
    Get view stats of a Page Title from Matomo.
    From_date_string & to_date_string must have YYYY-MM-DD format.
    The results are cached to speed up and avoid querying Matomo too often.
    """
    matomo_action_name = 'Actions.getPageTitle'
    matomo_page_title_base_url = 'https://stats.data.gouv.fr/index.php?idSite={}&module=API&method={}&pageName={}&period=range&date={},{}&format=json'.format(  # noqa
        settings.ANALYTICS_SITEID,
        matomo_action_name,
        page_title,
        from_date_string,
        to_date_string)

    res = requests.get(matomo_page_title_base_url)
    data = res.json()

    return data[0]
