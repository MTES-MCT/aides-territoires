from django.http import QueryDict


def clean_search_querystring(querystring):
    """
    - remove starting '?' if it exists
    - remove empty params
    """
    if not querystring:
        return querystring
    # Sometimes the querystring contains a leading '?' character
    # and we don't want it here.
    querystring = querystring.strip('?')
    # Re-build the querydict without the empty params
    querydict = QueryDict(querystring).copy()
    querydict_cleaned = QueryDict('', mutable=True)
    for k, v in querydict.lists():
        values_without_empty = list(filter(None, v))
        if values_without_empty:
            querydict_cleaned.setlist(k, values_without_empty)
    # Transform the cleaned querydict into a querystring
    querystring_cleaned = querydict_cleaned.urlencode()
    return querystring_cleaned
