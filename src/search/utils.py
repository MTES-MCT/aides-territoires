from django.http import QueryDict

from geofr.models import Perimeter
from categories.models import Theme, Category

from geofr.models import Perimeter
from categories.models import Theme, Category


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


def get_querystring_value_list_from_key(querystring, key):
    querydict = QueryDict(querystring)
    value_list = querydict.getlist(key)
    value_list_cleaned = list(filter(None, value_list))
    return value_list_cleaned


def get_querystring_perimeter(querystring):
    """
    We expect only 1 perimeter in the querystring
    Format ? It is prefixed with its 'id' (e.g. '71045-rhone')
    """
    PERIMETER_KEY = 'perimeter'
    perimeter_list = get_querystring_value_list_from_key(querystring, PERIMETER_KEY)  # noqa
    if len(perimeter_list):
        perimeter_id_str = perimeter_list[0].split('-')[0]
        return Perimeter.objects.get(id=perimeter_id_str)
    else:
        return None


def get_querystring_themes(querystring):
    THEMES_KEY = 'themes'
    themes_list = get_querystring_value_list_from_key(querystring, THEMES_KEY)
    return Theme.objects.filter(slug__in=themes_list)


def get_querystring_categories(querystring):
    CATEGORIES_KEY = 'categories'
    categories_list = get_querystring_value_list_from_key(querystring, CATEGORIES_KEY)  # noqa
    return Category.objects.filter(slug__in=categories_list)
