import requests
from functools import lru_cache

from django.conf import settings
from django.utils import timezone


GOAL_KEY = '_analytics_goal'


def track_goal(session, goal_id):
    """Set an analytics goal to be tracked."""
    session[GOAL_KEY] = goal_id


def get_goal(session):
    """Returns the currently tracked goal id.

    Also, clears the session, so we only track a specific goal using
    the js api once.
    """
    return session.pop(GOAL_KEY, '')


@lru_cache()
def get_matomo_stats_from_page_title(page_title, from_date_string, to_date_string=timezone.now().strftime('%Y-%m-%d'), result_key='nb_hits'):  # noqa
    """
    Get view stats of a Page Title from Matomo.
    from_date_string & to_date_string must have YYYY-MM-DD format.
    The results are cached to speed up and avoid querying Matomo too often.

    Usage example:
    get_matomo_stats_from_page_title('Les aides du programme Petites villes de demain', '2018-01-01', to_date_string='2020-12-31')  # noqa
    get_matomo_stats_from_page_title("Les dispositifs d'aides sur l'Arc de l'Innovation", '2018-01-01', to_date_string='2020-12-31')  # returns an error dict when the pageName has an appostrophe... # noqa
    """
    MATOMO_API_METHOD = 'Actions.getPageTitle'

    params = {
        'idSite': settings.ANALYTICS_SITEID,
        'module': 'API',
        'method': MATOMO_API_METHOD,
        'pageName': page_title,
        'period': 'range',
        'date': f'{from_date_string},{to_date_string}',
        'format': 'json'
    }
    res = requests.get(settings.ANALYTICS_ENDPOINT, params=params)
    data = res.json()

    # data should be an array
    if type(data) == list:
        if len(data):
            if result_key and (result_key in data[0]):
                return data[0][result_key]
            else:
                return data[0]
    return '-'


def get_matomo_page_urls_stats(from_date_string, to_date_string=timezone.now().strftime('%Y-%m-%d')):  # noqa
    """
    Get view stats of all Page Urls from Matomo.
    from_date_string & to_date_string must have YYYY-MM-DD format.

    Usage example:
    get_matomo_stats_from_page_title('2020-01-01', to_date_string='2020-12-31')
    """
    MATOMO_API_METHOD = 'Actions.getPageUrls'

    params = {
        'idSite': settings.ANALYTICS_SITEID,
        'module': 'API',
        'method': MATOMO_API_METHOD,
        'period': 'range',
        'date': f'{from_date_string},{to_date_string}',
        'flat': 1,
        'filter_limit': -1,
        'format': 'json'
    }
    res = requests.get(settings.ANALYTICS_ENDPOINT, params=params)
    data = res.json()

    # data should be an array
    return data
