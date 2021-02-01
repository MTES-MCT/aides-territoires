import pytest

from stats.models import AidSearchEvent
from aids.models import Aid
from categories.factories import ThemeFactory, CategoryFactory


pytestmark = pytest.mark.django_db


def test_model_create(perimeters):
    theme_1 = ThemeFactory(name='Nature environnement risques')
    theme_2 = ThemeFactory(name='Developpement economique')
    category_1 = CategoryFactory(name='economie circulaire')

    request_get_urlencoded = (
        "drafts=True&call_for_projects_only=False"
        "&targeted_audiences=department"
        f"&perimeter={perimeters['montpellier'].id_slug}"
        f"&themes={theme_1.slug}&themes={theme_2.slug}"
        f"&categories={category_1.slug}&categories=&apply_before=")

    event = AidSearchEvent.objects.create(querystring=request_get_urlencoded)

    assert not event.fields_populated
    assert event.results_count == 0
    assert event.targeted_audiences is None
    assert event.perimeter is None
    assert event.themes.count() == 0
    assert event.categories.count() == 0

    event.clean_and_populate_search_fields()

    assert event.fields_populated
    assert len(event.targeted_audiences) == 1
    assert event.targeted_audiences[0] == Aid.AUDIENCES.department
    assert event.perimeter == perimeters['montpellier']
    assert event.themes.count() == 2
    assert event.categories.count() == 1
