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
    From_date_string & to_date_string must have YYYY-MM-DD format.
    The results are cached to speed up and avoid querying Matomo too often.

    Usage example:
    get_matomo_stats_from_page_title('Les aides du programme Petites villes de demain', '2018-01-01', to_date_string='2020-12-31')  # noqa
    get_matomo_stats_from_page_title("Les dispositifs d'aides sur l'Arc de l'Innovation", '2018-01-01', to_date_string='2020-12-31')  # returns an error dict when the pageName has an appostrophe... # noqa
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

    # data should be an array
    if type(data) == list:
        if len(data):
            if result_key in data[0]:
                return data[0][result_key]
    return '-'
