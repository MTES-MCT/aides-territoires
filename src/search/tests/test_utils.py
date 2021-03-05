import pytest

from search.utils import (
    extract_id_from_string,
    clean_search_querystring,
    get_querystring_value_from_key, get_querystring_value_list_from_key,
    get_querystring_perimeter,
    # get_querystring_themes, get_querystring_categories
    get_querystring_backers, get_querystring_programs)
from backers.factories import BackerFactory
from programs.factories import ProgramFactory


pytestmark = pytest.mark.django_db


id_slug_string_testset = [
    ('', None),
    ('test', None),
    ('123', 123),
    ('123-', 123),
    ('123-test', 123),
]


@pytest.mark.parametrize('input_string,expected_cleaned_id', id_slug_string_testset)  # noqa
def test_extract_id_from_string(input_string, expected_cleaned_id):

    assert extract_id_from_string(input_string) == expected_cleaned_id


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


def test_get_querystring_perimeter_with_db(perimeters):
    assert get_querystring_perimeter('perimeter=france') is None
    assert get_querystring_perimeter(f"perimeter={perimeters['france'].id}") == perimeters['france']  # noqa
    assert get_querystring_perimeter(f"perimeter={perimeters['france'].id}-france") == perimeters['france']  # noqa


querystring_testset = [
    ('', []),
    ('drafts=True', []),
    ('backers=', []),
    ('backers=abc', []),
]


@pytest.mark.parametrize('input_querystring,expected_output', querystring_testset)  # noqa
def test_get_querystring_backers(input_querystring, expected_output):  # noqa

    assert list(get_querystring_backers(input_querystring)) == expected_output  # noqa


def test_get_querystring_backers_with_db():
    ademe = BackerFactory(name='ADEME')
    bpi = BackerFactory(name='Bpi France')

    assert list(get_querystring_backers(f"backers={ademe.slug}")) == []
    assert len(get_querystring_backers(f"backers={ademe.id}")) == 1
    assert get_querystring_backers(f"backers={ademe.id}")[0] == ademe
    assert get_querystring_backers(f"backers={ademe.id}-{ademe.slug}")[0] == ademe  # noqa
    assert len(get_querystring_backers(f"backers={ademe.id}&backers=")) == 1
    assert len(get_querystring_backers(f"backers={ademe.id}&backers={bpi.id}")) == 2  # noqa
    assert get_querystring_backers(f"backers={ademe.id}&backers={bpi.id}")[1] == bpi  # noqa
    assert get_querystring_backers(f"backers={bpi.id}&backers={ademe.id}")[1] == bpi  # ordered by id  # noqa


querystring_testset = [
    ('', []),
    ('drafts=True', []),
    ('programs=', []),
    ('programs=abc', []),
]


@pytest.mark.parametrize('input_querystring,expected_output', querystring_testset)  # noqa
def test_get_querystring_programs(input_querystring, expected_output):  # noqa

    assert list(get_querystring_programs(input_querystring)) == expected_output  # noqa


def test_get_querystring_programs_with_db():
    program_1 = ProgramFactory(name='Big plan')
    program_2 = ProgramFactory(name='Local plan')

    assert list(get_querystring_programs(f"programs={program_1.id}")) == []
    assert len(get_querystring_programs(f"programs={program_1.slug}")) == 1
    assert get_querystring_programs(f"programs={program_1.slug}")[0] == program_1  # noqa
    assert len(get_querystring_programs(f"programs={program_1.slug}&programs=")) == 1  # noqa
    assert len(get_querystring_programs(f"programs={program_1.slug}&programs={program_2.slug}")) == 2  # noqa
    assert get_querystring_programs(f"programs={program_1.slug}&programs={program_2.slug}")[1] == program_2  # noqa
    assert get_querystring_programs(f"programs={program_2.slug}&programs={program_1.slug}")[1] == program_2  # ordered by id  # noqa
