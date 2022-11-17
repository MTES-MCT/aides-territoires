import pytest

from django.urls import reverse

from stats.models import AidViewEvent, AidSearchEvent
from stats.utils import log_aidsearchevent
from aids.models import Aid
from aids.factories import AidFactory
from categories.factories import ThemeFactory, CategoryFactory
from backers.factories import BackerFactory
from programs.factories import ProgramFactory


pytestmark = pytest.mark.django_db


def test_log_aid_view_event(client):
    # user_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    aid = AidFactory()

    assert AidViewEvent.objects.count() == 0

    aid_url = reverse("aid_detail_view", args=[aid.slug])

    client.get(aid_url)  # HTTP_USER_AGENT=user_ua

    assert AidViewEvent.objects.count() == 1


def test_crawler_should_not_log_aid_view_event_stat(client):
    bot_ua = "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
    aid = AidFactory()

    assert AidViewEvent.objects.count() == 0

    aid_url = reverse("aid_detail_view", args=[aid.slug])

    client.get(aid_url, HTTP_USER_AGENT=bot_ua)

    assert AidViewEvent.objects.count() == 0


def test_scraper_should_not_log_aid_view_event_stat(client):
    scraper_referer = "https://aides-territoires.beta.gouv.fr/sitemap.xml"
    aid = AidFactory()

    assert AidViewEvent.objects.count() == 0

    aid_url = reverse("aid_detail_view", args=[aid.slug])

    # client.get(aid_url, headers={'referer': scraper_referer})
    client.get(aid_url, HTTP_REFERER=scraper_referer)

    assert AidViewEvent.objects.count() == 0


def test_log_aid_search_event(perimeters):
    theme_1 = ThemeFactory(name="Nature environnement risques")
    theme_2 = ThemeFactory(name="Developpement economique")
    category_1 = CategoryFactory(name="economie circulaire")
    # category_2 = CategoryFactory(name='musee')
    backer_1 = BackerFactory(name="ADEME")
    program_1 = ProgramFactory(name="Programme")

    request_get_urlencoded = (
        "drafts=True&call_for_projects_only=False&apply_before="
        "&targeted_audiences=department"
        f"&perimeter={perimeters['montpellier'].id_slug}"
        f"&themes={theme_1.slug}&themes={theme_2.slug}"
        f"&categories={category_1.slug}&categories="
        f"&backers={backer_1.id}-{backer_1.slug}"
        f"&programs={program_1.slug}"
    )
    results_count = 15
    host = "francemobilites.aides-territoires.beta.gouv.fr"

    log_aidsearchevent(
        querystring=request_get_urlencoded, results_count=results_count, source=host
    )

    event = AidSearchEvent.objects.last()

    assert len(event.targeted_audiences) == 1
    assert event.targeted_audiences[0] == Aid.AUDIENCES.department
    assert event.perimeter == perimeters["montpellier"]
    assert event.themes.count() == 2
    assert event.categories.count() == 1
    assert event.backers.count() == 1
    assert event.programs.count() == 1
    assert event.results_count == results_count
    assert event.source == "francemobilites"


def test_log_aid_search_event_with_wrong_targeted_audiences(perimeters):
    # wrong targeted_audiences
    request_get_urlencoded = "targeted_audiences=coucou"

    event_count_before = AidSearchEvent.objects.count()

    log_aidsearchevent(querystring=request_get_urlencoded)

    event_count_after = AidSearchEvent.objects.count()

    assert event_count_after == event_count_before

    # wrong targeted_audiences (real example)
    request_get_urlencoded = (
        "integration=test&text=test&perimeter=test"
        "&targeted_audiences=test&targeted_audiences=test"
        "&targeted_audiences=test&targeted_audiences=test"
        "&apply_before=test&call_for_projects_only=test"
        "&order_by=test+ORDER+BY+5040%23"
    )

    event_count_before = AidSearchEvent.objects.count()

    log_aidsearchevent(querystring=request_get_urlencoded)

    event_count_after = AidSearchEvent.objects.count()

    assert event_count_after == event_count_before

    # accepted targeted_audiences
    request_get_urlencoded = "targeted_audiences="

    event_count_before = AidSearchEvent.objects.count()

    log_aidsearchevent(querystring=request_get_urlencoded)

    event_count_after = AidSearchEvent.objects.count()

    assert event_count_after == event_count_before + 1

    # accepted targeted_audiences
    request_get_urlencoded = ""

    event_count_before = AidSearchEvent.objects.count()

    log_aidsearchevent(querystring=request_get_urlencoded)

    event_count_after = AidSearchEvent.objects.count()

    assert event_count_after == event_count_before + 1


def test_log_aid_search_event_with_internal(perimeters):
    theme_1 = ThemeFactory(name="Nature environnement risques")
    theme_2 = ThemeFactory(name="Developpement economique")
    category_1 = CategoryFactory(name="economie circulaire")

    request_get_urlencoded = (
        "drafts=True&call_for_projects_only=False"
        "&targeted_audiences=department"
        f"&perimeter={perimeters['montpellier'].id_slug}"
        f"&themes={theme_1.slug}&themes={theme_2.slug}"
        f"&categories={category_1.slug}&categories=&apply_before="
        "&internal=True"
    )

    event_count_before = AidSearchEvent.objects.count()

    log_aidsearchevent(querystring=request_get_urlencoded)

    event_count_after = AidSearchEvent.objects.count()

    assert event_count_after == event_count_before


def test_log_aid_search_event_with_pages(perimeters):
    # empty 'page' should work
    request_get_urlencoded = "page="
    event_count_before = AidSearchEvent.objects.count()
    log_aidsearchevent(querystring=request_get_urlencoded)
    event_count_after = AidSearchEvent.objects.count()
    assert event_count_after == event_count_before + 1

    # 'page=1' should work
    request_get_urlencoded = "page=1"
    event_count_before = AidSearchEvent.objects.count()
    log_aidsearchevent(querystring=request_get_urlencoded)
    event_count_after = AidSearchEvent.objects.count()
    assert event_count_after == event_count_before + 1

    # 'page=2' should not work
    request_get_urlencoded = "page=2"
    event_count_before = AidSearchEvent.objects.count()
    log_aidsearchevent(querystring=request_get_urlencoded)
    event_count_after = AidSearchEvent.objects.count()
    assert event_count_after == event_count_before

    # strange 'page=' should not work
    request_get_urlencoded = "page=coucou"
    event_count_before = AidSearchEvent.objects.count()
    log_aidsearchevent(querystring=request_get_urlencoded)
    event_count_after = AidSearchEvent.objects.count()
    assert event_count_after == event_count_before


def test_log_aid_search_event_empty(perimeters):

    request_get_urlencoded = ""

    log_aidsearchevent(querystring=request_get_urlencoded)

    event = AidSearchEvent.objects.last()

    assert event.targeted_audiences is None
    assert event.perimeter is None
    assert event.themes.count() == 0
    assert event.categories.count() == 0
    assert event.backers.count() == 0
    assert event.programs.count() == 0
    assert event.results_count == 0
    assert event.source == ""
