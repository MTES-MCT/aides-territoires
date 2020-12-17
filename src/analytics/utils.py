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

    try:
        return data[0][result_key]
    except KeyError:
        # most likely an error or missing information in the url
        return 0
