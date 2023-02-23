from crawlerdetect import CrawlerDetect

from core.celery import app
from core.utils import get_site_from_host
from search.utils import (
    clean_search_querystring,
    get_querystring_value_from_key,
    get_querystring_value_list_from_key,
    get_querystring_perimeter,
    get_querystring_themes,
    get_querystring_categories,
    get_querystring_backers,
    get_querystring_programs,
)
from stats.models import AidViewEvent, AidSearchEvent, Event
from aids.models import Aid
from accounts.models import User
from organizations.models import Organization


crawler_detect = CrawlerDetect()


@app.task
def log_aidviewevent(
    aid_id,
    user_pk=None,
    org_pk=None,
    querystring="",
    source="",
    request_ua="",
    request_referer="",
):
    source_cleaned = get_site_from_host(source)
    querystring_cleaned = clean_search_querystring(querystring)

    # There are some cases where we don't want to log the view event:
    # - a crawler (bot)
    # - a scraper (user script that parses & pulls data from our website)
    is_crawler = crawler_detect.isCrawler(request_ua)
    is_scraper = "sitemap.xml" in request_referer

    if not any([is_crawler, is_scraper]):
        targeted_audiences = (
            get_querystring_value_list_from_key(querystring, "targeted_audiences")
            or None
        )  # noqa
        if user_pk is not None and org_pk is not None:
            user = User.objects.get(pk=user_pk)
            org = Organization.objects.get(pk=org_pk)
            AidViewEvent.objects.create(
                aid_id=aid_id,
                user=user,
                organization=org,
                targeted_audiences=targeted_audiences,
                querystring=querystring_cleaned,
                source=source_cleaned,
            )
        else:
            AidViewEvent.objects.create(
                aid_id=aid_id,
                targeted_audiences=targeted_audiences,
                querystring=querystring_cleaned,
                source=source_cleaned,
            )


@app.task
def log_aidsearchevent(querystring="", results_count=0, source="", request_ua=""):
    """
    Method to cleanup/populate the AidSearchEvents
    Run asynchronously to avoid slowing down requests.
    """
    source_cleaned = get_site_from_host(source)
    querystring_cleaned = clean_search_querystring(querystring)

    # There are some cases where we don't want to log the search event:
    # - a crawler
    # - when there are unknown targeted_audiences (e.g. 'test', since May 2021)
    # - when we query our API for internal (e.g. admin) purposes
    # - page is greater than 1 (the user has scrolled to see more results) or has a strange value
    is_crawler = crawler_detect.isCrawler(request_ua)
    targeted_audiences = (
        get_querystring_value_list_from_key(querystring, "targeted_audiences") or None
    )  # noqa
    is_wrong_search = (
        targeted_audiences
        and len(targeted_audiences)
        and targeted_audiences[0] not in Aid.AUDIENCES
    )  # noqa
    is_internal_search = get_querystring_value_list_from_key(
        querystring_cleaned, "internal"
    )
    next_page = get_querystring_value_from_key(querystring_cleaned, "page")
    is_next_page_search = next_page and (not next_page.isdigit() or int(next_page) > 1)

    if not any([is_crawler, is_wrong_search, is_internal_search, is_next_page_search]):
        perimeter = get_querystring_perimeter(querystring)
        text = get_querystring_value_from_key(querystring, "text")

        event = AidSearchEvent.objects.create(
            querystring=querystring_cleaned,
            source=source_cleaned,
            results_count=results_count,
            targeted_audiences=targeted_audiences,
            perimeter=perimeter,
            text=text,
        )

        themes = get_querystring_themes(querystring)
        categories = get_querystring_categories(querystring)
        backers = get_querystring_backers(querystring)
        programs = get_querystring_programs(querystring)
        event.themes.set(themes)
        event.categories.set(categories)
        event.backers.set(backers)
        event.programs.set(programs)


def log_event(category, event, meta="", source="", value=None):
    Event.objects.create(
        category=category, event=event, meta=meta, source=source, value=value
    )
