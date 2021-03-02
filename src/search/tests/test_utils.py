from search.utils import (
    clean_search_querystring, get_querystring_value_list_from_key,
    get_querystring_perimeter)
# get_querystring_themes, get_querystring_categories)


def test_clean_search_querystring():
    querystring_testset = [
        # ('some-querystring', 'expected-cleaned-querystring')
        ('', ''),  # expecting nothing
        ('drafts=True&call_for_projects_only=False', 'drafts=True&call_for_projects_only=False'),  # noqa
        ('?drafts=True', 'drafts=True'),  # expecting '?' removed
        ('text=', ''),  # expecting empty fields to be cleaned up
        ('integration=&apply_before=', ''),
        ('text=&order_by=relevance&perimeter=', 'order_by=relevance'),
        ('theme=culture-sports&category=musee&category=sport&category=', 'theme=culture-sports&category=musee&category=sport'),  # noqa
    ]
    for querystring in querystring_testset:
        assert clean_search_querystring(querystring[0]) == querystring[1]


def test_get_querystring_value_list_from_key():
    querystring_testset = [
        ('', 'draft', []),
        ('draft=', 'draft', []),
        ('internal=True', 'internal', ['True']),
        ('category=musee', 'category', ['musee']),
        ('category=musee&category=', 'category', ['musee']),
        ('category=musee&category=livres', 'category', ['musee', 'livres']),
        ('category=musee', 'theme', []),
    ]
    for querystring in querystring_testset:
        assert get_querystring_value_list_from_key(querystring[0], querystring[1]) == querystring[2]  # noqa


def test_get_querystring_perimeter():
    querystring_testset = [
        ('', None),
        ('drafts=True', None),
        ('perimeter=', None)
    ]
    for querystring in querystring_testset:
        assert get_querystring_perimeter(querystring[0]) == querystring[1]
