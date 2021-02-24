from django.http import QueryDict
from django.utils.datastructures import MultiValueDict


def clean_search_querystring(querystring):
    """
    - remove starting ? if it exists
    - remove empty params
    """
    if querystring:
        # Remove starting '?' if it exists
        if querystring.startswith('?'):
            querystring = querystring[1:]
        if len(querystring):
            # Remove empty params
            querydict = QueryDict(querystring).copy()
            dict_cleaned = dict()
            for k, v in querydict.lists():
                v = list(filter(None, v))
                if len(v):
                    dict_cleaned[k] = v
            # Rebuild querystring
            querydict_cleaned = QueryDict('', mutable=True)
            querydict_cleaned.update(MultiValueDict(dict_cleaned))
            querystring = querydict_cleaned.urlencode()
    return querystring
