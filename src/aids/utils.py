import requests
from django.db.models.query import QuerySet

from geofr.utils import get_all_related_perimeters
from geofr.models import Perimeter
from aids.models import Aid


def filter_generic_aids(qs: QuerySet, search_perimeter: Perimeter = None) -> QuerySet:
    """
    We should never have both the generic aid and its local version
    together on search results.
    Which one should be removed from the result ? It depends...
    We consider the scale perimeter associated to the local aid.
    - When searching on a wider area than the local aid's perimeter,
        then we display the generic version.
    - When searching on a smaller area than the local aid's perimeter,
        then we display the local version.
    """

    # We will consider local aids for which the associated generic
    # aid is listed in the results - We should consider excluding a
    # local aid, only when it's generic aid is listed.
    generic_aids = qs.generic_aids()
    local_aids = qs.local_aids().filter(generic_aid__in=generic_aids)
    # We use a python list for better performance
    local_aids_list = local_aids.values_list(
        "pk", "perimeter__scale", "generic_aid__pk"
    )

    aids_to_exclude = []
    if not search_perimeter:
        # If the user does not specify a search perimeter, then we go wide.
        search_smaller = False
        search_wider = True
    for aid_id, perimeter_scale, generic_aid_id in local_aids_list:
        if search_perimeter:
            search_smaller = search_perimeter.scale <= perimeter_scale
            search_wider = search_perimeter.scale > perimeter_scale
        # If the search perimeter is smaller or matches exactly the local
        # perimeter, then it's relevant to keep the local and exclude
        # the generic aid.Excluding the generic aid takes precedence
        # over excluding the local aid.
        if search_smaller:
            aids_to_exclude.append(generic_aid_id)
        elif search_wider:
            # If the search perimeter is wider than the local perimeter
            # then it more relevant to keep the generic aid and exclude the
            # the local one.
            aids_to_exclude.append(aid_id)

    # If the local aid is expired the search perimeter is smaller or matches
    # exactly the local perimeter then its relevant to not displayed local aid
    # AND the generic aid
    if search_perimeter is not None:
        perimeter_ids = get_all_related_perimeters(search_perimeter.id, values=["id"])

        local_aids_expired = (
            Aid.objects.local_aids()
            .filter(generic_aid__in=generic_aids, perimeter__in=perimeter_ids)
            .expired()
            .published()
        )
        # We use a python list for better performance
        local_aids_expired_list = local_aids_expired.values_list(
            "pk", "perimeter__scale", "generic_aid__pk"
        )
        for aid_id, perimeter_scale, generic_aid_id in local_aids_expired_list:
            if search_perimeter:
                search_smaller = search_perimeter.scale <= perimeter_scale
            if search_smaller:
                aids_to_exclude.append(generic_aid_id)

    qs = qs.exclude(pk__in=aids_to_exclude)
    return qs


def check_if_url_return_an_error(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",  # noqa
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return True
    except Exception:
        return True
