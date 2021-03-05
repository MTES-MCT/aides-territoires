import pytest

from search.utils import (
    clean_search_querystring,
    get_querystring_value_from_key, get_querystring_value_list_from_key,
    get_querystring_perimeter)
# get_querystring_themes, get_querystring_categories)


pytestmark = pytest.mark.django_db


querystring_testset = [
    ('', ''),  # expecting nothing
    ('drafts=True&call_for_projects_only=False', 'drafts=True&call_for_projects_only=False'),  # noqa
    ('?drafts=True', 'drafts=True'),  # expecting '?' removed
    ('text=', ''),  # expecting empty fields to be cleaned up
    ('integration=&apply_before=', ''),
    ('text=&order_by=relevance&perimeter=', 'order_by=relevance'),
    ('theme=culture-sports&category=musee&category=sport&category=', 'theme=culture-sports&category=musee&category=sport'),  # noqa
]


@pytest.mark.parametrize('input_querystring,expected_cleaned_querystring', querystring_testset)  # noqa
def test_clean_search_querystring(input_querystring, expected_cleaned_querystring):  # noqa

    assert clean_search_querystring(input_querystring) == expected_cleaned_querystring  # noqa


querystring_testset = [
    ('', 'draft', None),
    ('draft=', 'draft', ''),
    ('internal=True', 'internal', 'True'),
    ('category=musee', 'category', 'musee'),
    ('category=musee&category=', 'category', ''),
    ('category=musee&category=livres', 'category', 'livres'),
    ('category=livres&category=musee', 'category', 'musee'),
    ('category=musee', 'theme', None),
]


@pytest.mark.parametrize('input_querystring,key,expected_output', querystring_testset)  # noqa
def test_get_querystring_value_from_key(input_querystring, key, expected_output):  # noqa

    assert get_querystring_value_from_key(input_querystring, key) == expected_output  # noqa


querystring_testset = [
    ('', 'draft', []),
    ('draft=', 'draft', []),
    ('internal=True', 'internal', ['True']),
    ('category=musee', 'category', ['musee']),
    ('category=musee&category=', 'category', ['musee']),
    ('category=musee&category=livres', 'category', ['musee', 'livres']),
    ('category=musee', 'theme', []),
]


@pytest.mark.parametrize('input_querystring,key,expected_output', querystring_testset)  # noqa
def test_get_querystring_value_list_from_key(input_querystring, key, expected_output):  # noqa

    assert get_querystring_value_list_from_key(input_querystring, key) == expected_output  # noqa


querystring_testset = [
    ('', None),
    ('drafts=True', None),
    ('perimeter=', None),
    ('perimeter=abc', None),
]


@pytest.mark.parametrize('input_querystring,expected_output', querystring_testset)  # noqa
def test_get_querystring_perimeter(input_querystring, expected_output):  # noqa

    assert get_querystring_perimeter(input_querystring) == expected_output  # noqa


def test_get_querystring_perimeter_with_fixture(perimeters):
    assert get_querystring_perimeter('perimeter=france') is None
    assert get_querystring_perimeter(f"perimeter={perimeters['france'].id}") == perimeters['france']  # noqa
    assert get_querystring_perimeter(f"perimeter={perimeters['france'].id}-france") == perimeters['france']  # noqa
