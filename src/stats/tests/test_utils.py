import pytest

from stats.models import AidSearchEvent
from stats.utils import log_aidsearchevent
from aids.models import Aid
from categories.factories import ThemeFactory, CategoryFactory


pytestmark = pytest.mark.django_db


def test_log_aid_search_event(perimeters):
    theme_1 = ThemeFactory(name='Nature environnement risques')
    theme_2 = ThemeFactory(name='Developpement economique')
    category_1 = CategoryFactory(name='economie circulaire')

    request_get_urlencoded = (
        "drafts=True&call_for_projects_only=False"
        "&targeted_audiences=department"
        f"&perimeter={perimeters['montpellier'].id_slug}"
        f"&themes={theme_1.slug}&themes={theme_2.slug}"
        f"&categories={category_1.slug}&categories=&apply_before=")
    results_count = 15
    host = "francemobilites.aides-territoires.beta.gouv.fr"

    log_aidsearchevent(
        querystring=request_get_urlencoded,
        results_count=results_count,
        source=host)

    event = AidSearchEvent.objects.last()

    assert len(event.targeted_audiences) == 1
    assert event.targeted_audiences[0] == Aid.AUDIENCES.department
    assert event.perimeter == perimeters['montpellier']
    assert event.themes.count() == 2
    assert event.results_count == results_count
    assert event.source == 'francemobilites'


def test_log_aid_search_event_with_internal(perimeters):
    theme_1 = ThemeFactory(name='Nature environnement risques')
    theme_2 = ThemeFactory(name='Developpement economique')
    category_1 = CategoryFactory(name='economie circulaire')

    request_get_urlencoded = (
        "drafts=True&call_for_projects_only=False"
        "&targeted_audiences=department"
        f"&perimeter={perimeters['montpellier'].id_slug}"
        f"&themes={theme_1.slug}&themes={theme_2.slug}"
        f"&categories={category_1.slug}&categories=&apply_before="
        "&internal=True")

    event_count_before = AidSearchEvent.objects.count()

    log_aidsearchevent(querystring=request_get_urlencoded)

    event_count_after = AidSearchEvent.objects.count()

    assert event_count_before == event_count_after


def test_log_aid_search_event_empty(perimeters):

    request_get_urlencoded = ""

    log_aidsearchevent(querystring=request_get_urlencoded)

    event = AidSearchEvent.objects.last()

    assert event.targeted_audiences is None
    assert event.perimeter is None
    assert event.themes.count() == 0
    assert event.categories.count() == 0
    assert event.results_count == 0
    assert event.source == ''
