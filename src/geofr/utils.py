import collections

from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from geofr.constants import OVERSEAS_PREFIX, DEPARTMENT_TO_REGION
from geofr.models import Perimeter


def department_from_zipcode(zipcode):
    """Extracts the department code from the given (valid) zipcode."""

    if zipcode.startswith(OVERSEAS_PREFIX):
        prefix = zipcode[:3]
    else:
        prefix = zipcode[:2]
    return prefix


def region_from_zipcode(zipcode):
    """Extracts the region code from the given zipcode."""

    department = department_from_zipcode(zipcode)
    return DEPARTMENT_TO_REGION[department]


def is_overseas(zipcode):
    """Tell if the given zipcode is overseas or mainland."""

    return zipcode.startswith(OVERSEAS_PREFIX)


def extract_perimeters_from_file(perimeter_list_file):
    item_list = []

    # extract items
    for line in perimeter_list_file:
        try:
            item = line.decode().strip().split(';')[0]
            clean_item = str(item)
            item_list.append(clean_item)
        except (UnicodeDecodeError, ValueError) as e:
            msg = _('This file seems invalid. \
                    Please double-check its content or contact the \
                    dev team if you feel like it\'s an error. \
                    Here is the original error: {}').format(e)
            raise Exception(msg)

    # check for duplicates
    duplicates = [item for item, count in \
        collections.Counter(item_list).items() if count > 1]
    if len(duplicates):
        msg = _('This file is valid, but contains \
                duplicates: {}').format(duplicates)
        raise Exception(msg)

    return item_list


def query_cities_from_list(city_codes_list):
    return Perimeter.objects \
        .filter(code__in=city_codes_list) \
        .filter(scale=Perimeter.TYPES.commune)


def query_epcis_from_list(epci_names_list):
    return Perimeter.objects \
        .filter(name__in=epci_names_list) \
        .filter(scale=Perimeter.TYPES.epci)


def attach_epci_perimeters(adhoc, epci_names):
    # first get the epci_query from the epci_names list
    epci_query = query_epcis_from_list(epci_names)
    # get the city_codes list from these epci perimeters
    city_codes = combine_perimeters(epci_query, [])
    # finally call the usual attach_perimeters method
    attach_perimeters(adhoc, city_codes)


@transaction.atomic
def attach_perimeters(adhoc, city_codes):
    """Attach an ad-hoc perimeter to other perimeters.

    This function makes sure the `adhoc` perimeter is added to the
    `contained_in` list of all perimeters corresponding to the `city_codes`.

    E.g if we want to attach the "Communes littorales" Ad-hoc perimeter to the
    "Vic-la-Gardiole" city perimeter, we add "Communes littorales" to
    "Vic-la-Gardiole".contained_in, but also to "Herault".contained_in,
    "Occitanie".contained_in…
    """
    # Delete existing links
    PerimeterContainedIn = Perimeter.contained_in.through
    PerimeterContainedIn.objects \
        .filter(to_perimeter_id=adhoc.id) \
        .delete()

    # Fetch perimeters corresponding to the given city codes
    perimeters = query_cities_from_list(city_codes) \
        .prefetch_related('contained_in')

    # Put the adhoc perimeter in the cities `contained_in` lists
    containing = []
    for perimeter in perimeters:
        containing.append(PerimeterContainedIn(
            from_perimeter_id=perimeter.id,
            to_perimeter_id=adhoc.id))

        # Perimeters that contain the cities must contain the adhoc perimeter
        # except for France and Europe.
        for container in perimeter.contained_in.all():
            if container != adhoc and container.scale <= Perimeter.TYPES.adhoc:
                containing.append(PerimeterContainedIn(
                    from_perimeter_id=container.id,
                    to_perimeter_id=adhoc.id))

    # Bulk create the links
    PerimeterContainedIn.objects.bulk_create(
        containing, ignore_conflicts=True)


def combine_perimeters(add_perimeters, rm_perimeters):
    """Combine perimeters to extract some city codes.

    Return the city codes that are in `add_perimeters` and not in
    `rm_perimeters`.
    """
    print(add_perimeters)
    in_city_codes = Perimeter.objects \
        .filter(scale=Perimeter.TYPES.commune) \
        .filter(contained_in__in=add_perimeters) \
        .values_list('code', flat=True)

    out_city_codes = Perimeter.objects \
        .filter(scale=Perimeter.TYPES.commune) \
        .filter(contained_in__in=rm_perimeters) \
        .values_list('code', flat=True)

    return set(in_city_codes) - set(out_city_codes)
