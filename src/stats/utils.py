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
    get_querystring_text,
    get_querystring_project_types,
)
from stats.models import (
    AidViewEvent,
    AidSearchEvent,
    BackerViewEvent,
    Event,
    ContactFormSendEvent,
    PostViewEvent,
    ProgramViewEvent,
    PublicProjectSearchEvent,
    PublicProjectViewEvent,
    ValidatedProjectSearchEvent,
)
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
def log_aidsearchevent(
    querystring="",
    results_count=0,
    source="",
    request_ua="",
    user_pk=None,
    org_pk=None,
):
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

        if user_pk is not None and org_pk is not None:
            user = User.objects.get(pk=user_pk)
            org = Organization.objects.get(pk=org_pk)
            event = AidSearchEvent.objects.create(
                user=user,
                organization=org,
                querystring=querystring_cleaned,
                source=source_cleaned,
                results_count=results_count,
                targeted_audiences=targeted_audiences,
                perimeter=perimeter,
                text=text,
            )

        else:
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


@app.task
def log_contactformsendevent(subject):
    ContactFormSendEvent.objects.create(subject=subject)


@app.task
def log_publicprojectviewevent(
    project_id,
    user_pk=None,
    org_pk=None,
    request_ua="",
    request_referer="",
):

    # There are some cases where we don't want to log the view event:
    # - a crawler (bot)
    # - a scraper (user script that parses & pulls data from our website)
    is_crawler = crawler_detect.isCrawler(request_ua)
    is_scraper = "sitemap.xml" in request_referer

    if not any([is_crawler, is_scraper]):
        if user_pk is not None and org_pk is not None:
            user = User.objects.get(pk=user_pk)
            org = Organization.objects.get(pk=org_pk)
            PublicProjectViewEvent.objects.create(
                project_id=project_id,
                user=user,
                organization=org,
            )
        else:
            PublicProjectViewEvent.objects.create(
                project_id=project_id,
            )


@app.task
def log_validatedprojectsearchevent(
    querystring="",
    results_count=0,
    user_pk=None,
    org_pk=None,
    request_ua="",
):

    """
    Method to cleanup/populate the AidSearchEvents
    Run asynchronously to avoid slowing down requests.
    """
    querystring_cleaned = clean_search_querystring(querystring)

    # There are some cases where we don't want to log the search event:
    # - a crawler
    # - page is greater than 1 (the user has scrolled to see more results) or has a strange value
    is_crawler = crawler_detect.isCrawler(request_ua)
    is_internal_search = get_querystring_value_list_from_key(
        querystring_cleaned, "internal"
    )
    next_page = get_querystring_value_from_key(querystring_cleaned, "page")
    is_next_page_search = next_page and (not next_page.isdigit() or int(next_page) > 1)

    if not any([is_crawler, is_internal_search, is_next_page_search]):
        perimeter = get_querystring_perimeter(querystring, "project_perimeter")
        text = get_querystring_text(querystring)

        if user_pk is not None and org_pk is not None:
            user = User.objects.get(pk=user_pk)
            org = Organization.objects.get(pk=org_pk)
            ValidatedProjectSearchEvent.objects.create(
                user=user,
                organization=org,
                querystring=querystring_cleaned,
                results_count=results_count,
                perimeter=perimeter,
                text=text,
            )

        else:
            ValidatedProjectSearchEvent.objects.create(
                querystring=querystring_cleaned,
                results_count=results_count,
                perimeter=perimeter,
                text=text,
            )


@app.task
def log_publicprojectsearchevent(
    querystring="",
    results_count=0,
    user_pk=None,
    org_pk=None,
    request_ua="",
):

    """
    Method to cleanup/populate the AidSearchEvents
    Run asynchronously to avoid slowing down requests.
    """
    querystring_cleaned = clean_search_querystring(querystring)

    # There are some cases where we don't want to log the search event:
    # - a crawler
    # - page is greater than 1 (the user has scrolled to see more results) or has a strange value
    is_crawler = crawler_detect.isCrawler(request_ua)
    is_internal_search = get_querystring_value_list_from_key(
        querystring_cleaned, "internal"
    )
    next_page = get_querystring_value_from_key(querystring_cleaned, "page")
    is_next_page_search = next_page and (not next_page.isdigit() or int(next_page) > 1)

    if not any([is_crawler, is_internal_search, is_next_page_search]):
        perimeter = get_querystring_perimeter(querystring, "project_perimeter")

        if user_pk is not None and org_pk is not None:
            user = User.objects.get(pk=user_pk)
            org = Organization.objects.get(pk=org_pk)
            event = PublicProjectSearchEvent.objects.create(
                user=user,
                organization=org,
                querystring=querystring_cleaned,
                results_count=results_count,
                perimeter=perimeter,
            )

        else:
            event = PublicProjectSearchEvent.objects.create(
                querystring=querystring_cleaned,
                results_count=results_count,
                perimeter=perimeter,
            )

        project_types = get_querystring_project_types(querystring)
        event.project_types.set(project_types)


@app.task
def log_programviewevent(
    program_id,
    user_pk=None,
    org_pk=None,
    source="",
    request_ua="",
    request_referer="",
):
    source_cleaned = get_site_from_host(source)

    # There are some cases where we don't want to log the view event:
    # - a crawler (bot)
    # - a scraper (user script that parses & pulls data from our website)
    is_crawler = crawler_detect.isCrawler(request_ua)
    is_scraper = "sitemap.xml" in request_referer

    if not any([is_crawler, is_scraper]):
        if user_pk is not None and org_pk is not None:
            user = User.objects.get(pk=user_pk)
            org = Organization.objects.get(pk=org_pk)
            ProgramViewEvent.objects.create(
                program_id=program_id,
                user=user,
                organization=org,
                source=source_cleaned,
            )
        else:
            ProgramViewEvent.objects.create(
                program_id=program_id,
                source=source_cleaned,
            )


@app.task
def log_backerviewevent(
    backer_id,
    user_pk=None,
    org_pk=None,
    source="",
    request_ua="",
    request_referer="",
):
    source_cleaned = get_site_from_host(source)

    # There are some cases where we don't want to log the view event:
    # - a crawler (bot)
    # - a scraper (user script that parses & pulls data from our website)
    is_crawler = crawler_detect.isCrawler(request_ua)
    is_scraper = "sitemap.xml" in request_referer

    if not any([is_crawler, is_scraper]):
        if user_pk is not None and org_pk is not None:
            user = User.objects.get(pk=user_pk)
            org = Organization.objects.get(pk=org_pk)
            BackerViewEvent.objects.create(
                backer_id=backer_id,
                user=user,
                organization=org,
                source=source_cleaned,
            )
        else:
            BackerViewEvent.objects.create(
                backer_id=backer_id,
                source=source_cleaned,
            )


@app.task
def log_postviewevent(
    post_id,
    user_pk=None,
    org_pk=None,
    request_ua="",
    request_referer="",
):

    # There are some cases where we don't want to log the view event:
    # - a crawler (bot)
    # - a scraper (user script that parses & pulls data from our website)
    is_crawler = crawler_detect.isCrawler(request_ua)
    is_scraper = "sitemap.xml" in request_referer

    if not any([is_crawler, is_scraper]):
        if user_pk is not None and org_pk is not None:
            user = User.objects.get(pk=user_pk)
            org = Organization.objects.get(pk=org_pk)
            PostViewEvent.objects.create(
                post_id=post_id,
                user=user,
                organization=org,
            )
        else:
            PostViewEvent.objects.create(
                post_id=post_id,
            )
