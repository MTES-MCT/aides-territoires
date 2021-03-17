from django.http import QueryDict

from geofr.models import Perimeter
from categories.models import Theme, Category
from backers.models import Backer


def extract_id_from_string(id_slug_str):
    """
    For some models, we concatenate the objects id with their slug
    Example: '22-ademe'
    """
    id_str = id_slug_str.split('-')[0]
    try:
        return int(id_str)
    except:  # noqa
        return None


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


def get_querystring_value_from_key(querystring, key):
    querydict = QueryDict(querystring)
    value = querydict.get(key)
    return value


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
        try:
            perimeter_id = extract_id_from_string(perimeter_list[0])
            return Perimeter.objects.get(id=perimeter_id)
        except Exception:
            return None
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


def get_querystring_backers(querystring):
    BACKERS_KEY = 'backers'
    backers_list = get_querystring_value_list_from_key(querystring, BACKERS_KEY)  # noqa
    backers_list_id_str = [extract_id_from_string(backer) for backer in backers_list]  # noqa
    return Backer.objects.filter(id__in=backers_list_id_str)
