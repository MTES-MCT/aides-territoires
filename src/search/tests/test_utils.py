from search.utils import clean_search_querystring


def test_clean_search_querystring():
    querystring_testset = [
        # (querystring, querystring_cleaned)
        # nothing to do
        ('', ''),
        ('drafts=True&call_for_projects_only=False', 'drafts=True&call_for_projects_only=False'),  # noqa
        # remove '?'
        ('?drafts=True', 'drafts=True'),
        # clean empty fields
        ('text=', ''),
        ('integration=&apply_before=', ''),
        ('text=&perimeter=&order_by=relevance', 'order_by=relevance'),
        ('theme=culture-patrimoine-sports-tourisme&category=musee&category=', 'theme=culture-patrimoine-sports-tourisme&category=musee'),  # noqa
    ]
    for querystring in querystring_testset:
        assert clean_search_querystring(querystring[0]) == querystring[1]
