from django.http import QueryDict

from geofr.models import Perimeter
from categories.models import Theme, Category
from backers.models import Backer
from programs.models import Program
from keywords.models import SynonymList


SEARCH_EXTRA_FIELDS = ["integration", "order_by", "action"]


def extract_id_from_string(id_slug_str):
    """
    For some models, we display in the querystring
    the concatenation of the object's id with their slug
    Example: '22-ademe'
    """
    id_str = id_slug_str.split("-")[0]
    try:
        return int(id_str)
    except Exception:
        return None


def clean_search_form(search_form, remove_extra_fields=False):
    """
    By cleaning the form, we can detect if it is empty for example.
    """
    # Keep only keys with a value
    search_form_dict = {k: v for k, v in search_form.items() if v}
    # Remove extra fields
    if remove_extra_fields:
        search_form_dict = {
            k: v for k, v in search_form_dict.items() if k not in SEARCH_EXTRA_FIELDS
        }
    return search_form_dict


def clean_search_querystring(
    querystring, remove_extra_fields=False, return_querydict=False
):  # noqa
    """
    - remove starting '?' if it exists
    - remove empty params
    """
    if not querystring:
        return querystring
    # Sometimes the querystring contains a leading '?' character
    # and we don't want it here.
    querystring = querystring.strip("?")
    # Re-build the querydict without the empty params
    querydict = QueryDict(querystring).copy()
    querydict_cleaned = QueryDict("", mutable=True)
    for k, v in querydict.lists():
        values_without_empty = list(filter(None, v))
        if values_without_empty:
            if not remove_extra_fields or (
                remove_extra_fields
                and (
                    k not in SEARCH_EXTRA_FIELDS and values_without_empty[0] != "False"
                )
            ):
                querydict_cleaned.setlist(k, values_without_empty)
    if return_querydict:
        return querydict_cleaned
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


def get_querystring_perimeter(querystring, key="perimeter"):
    """
    Format ? 'id-slug' (e.g. '71045-rhone')
    Returns None or 1 perimeter
    """
    PERIMETER_KEY = key
    perimeter_list = get_querystring_value_list_from_key(querystring, PERIMETER_KEY)
    if len(perimeter_list):
        try:
            perimeter_id = extract_id_from_string(perimeter_list[0])
            return Perimeter.objects.get(id=perimeter_id)
        except Exception:
            return None
    else:
        return None


def get_querystring_text(querystring):

    TEXT_KEY = "text"
    text = get_querystring_value_list_from_key(querystring, TEXT_KEY)
    if text:
        try:
            synonymlist_id = extract_id_from_string(text[0])
            return SynonymList.objects.get(id=synonymlist_id).keywords_list
        except Exception:
            return text[0]
    else:
        return None


def get_querystring_themes(querystring):
    """
    Format ? 'slug'
    Returns a QuerySet
    """
    THEMES_KEY = "themes"
    themes_list = get_querystring_value_list_from_key(querystring, THEMES_KEY)
    return Theme.objects.filter(slug__in=themes_list)


def get_querystring_categories(querystring):
    """
    Format ? 'slug'
    Returns a QuerySet
    """
    CATEGORIES_KEY = "categories"
    categories_list = get_querystring_value_list_from_key(querystring, CATEGORIES_KEY)
    return Category.objects.filter(slug__in=categories_list)


def get_querystring_backers(querystring):
    """
    Format ? 'id-slug'
    Returns a QuerySet
    """
    BACKERS_KEY = "backers"
    backers_list = get_querystring_value_list_from_key(querystring, BACKERS_KEY)
    backers_list_id = [extract_id_from_string(backer) for backer in backers_list]
    return Backer.objects.filter(id__in=backers_list_id)


def get_querystring_programs(querystring):
    """
    Format ? 'slug'
    Returns a QuerySet
    """
    PROGRAMS_KEY = "programs"
    programs_list = get_querystring_value_list_from_key(querystring, PROGRAMS_KEY)
    return Program.objects.filter(slug__in=programs_list)
