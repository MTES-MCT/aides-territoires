import requests
from django.apps import apps
from django.db.models.query import QuerySet

from geofr.utils import get_all_related_perimeters
from geofr.models import Perimeter
from aids.models import Aid


def filter_generic_aids(  # NOSONAR
    qs: QuerySet, search_perimeter: Perimeter = None
) -> QuerySet:
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


def check_if_url_returns_an_error(url: str) -> bool:
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",  # noqa
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return True
        else:
            return False
    except Exception:
        return True


def prepopulate_ds_folder(ds_mapping, user, org):  # NOSONAR
    data = {}

    for field in ds_mapping["FieldsList"]:
        if field["response_value"] is not None:
            data[field["ds_field_id"]] = field["response_value"]
        elif (
            field["at_app"] is not None
            and field["at_model"] is not None
            and field["at_model_attr"] is not None
        ):
            at_model = apps.get_model(field["at_app"], field["at_model"])
            at_field = field["at_model_attr"]
            at_field_type = at_model._meta.get_field(at_field).get_internal_type()
            if field["at_model"] == "User":
                if at_field_type == "CharField":
                    if user._meta.get_field(at_field).choices:
                        at_field_value = getattr(user, "get_%s_display" % at_field)()
                    else:
                        at_field_value = getattr(user, at_field)
                else:
                    at_field_value = getattr(user, at_field)
                data[field["ds_field_id"]] = at_field_value
            elif field["at_model"] == "Organization":
                at_field_value = getattr(org, at_field)
                if at_field == "organization_type":
                    if org.organization_type is not None:
                        if field["choices_mapping"]:
                            at_field_value = field["choices_mapping"][at_field_value[0]]
                            data[field["ds_field_id"]] = at_field_value
                else:
                    data[field["ds_field_id"]] = at_field_value
    return data
