from search.utils import clean_search_querystring


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
