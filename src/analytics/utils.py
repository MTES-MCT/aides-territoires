import requests
from functools import lru_cache

from django.conf import settings
from django.utils import timezone


MATOMO_GET_PAGE_URLS_API_METHOD = "Actions.getPageUrls"
MATOMO_GET_PAGE_TITLES_API_METHOD = "Actions.getPageTitles"
MATOMO_GET_PAGE_TITLE_API_METHOD = "Actions.getPageTitle"
GOAL_KEY = "_analytics_goal"


def track_goal(session, goal_id):
    """Set an analytics goal to be tracked."""
    session[GOAL_KEY] = goal_id


def get_goal(session):
    """Returns the currently tracked goal id.

    Also, clears the session, so we only track a specific goal using
    the js api once.
    """
    return session.pop(GOAL_KEY, "")


@lru_cache()
def get_matomo_stats(
    api_method, custom_segment="", from_date_string="2020-01-01", to_date_string=None
):
    """
    Get stats of all Page Urls from Matomo.
    from_date_string & to_date_string must have YYYY-MM-DD format.

    API Method examples:
    - 'Actions.getPageUrls' (views per page url)
    - 'Actions.getPageTitles' (views per page title)
    - 'Actions.getSiteSearchKeywords' (keywords searched in the the application)

    Custom segments examples:
    https://developer.matomo.org/api-reference/reporting-api-segmentation
    - 'pageUrl=@actioncoeurdeville.aides-territoires.beta.gouv.fr' (url must contain string)
    - 'pageTitle==Aides-territoires | Recherche avancée'

    Usage example:
    get_matomo_stats_from_page_title('Actions.getPageUrls', from_date_string='2020-01-01', to_date_string='2020-12-31')  # noqa
    """  # noqa
    if to_date_string is None:
        to_date_string = timezone.now().strftime("%Y-%m-%d")

    params = {
        "idSite": settings.ANALYTICS_SITEID,
        "module": "API",
        "method": api_method,
        "period": "range",
        "date": f"{from_date_string},{to_date_string}",
        "flat": 1,
        "filter_limit": -1,
        "format": "json",
        "segment": custom_segment,
    }
    res = requests.get(settings.ANALYTICS_ENDPOINT, params=params)
    data = res.json()

    # data should be an array if successful
    # else it will be a dict {'result': 'error', 'message': '...'}
    return data
