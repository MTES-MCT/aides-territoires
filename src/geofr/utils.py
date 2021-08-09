import collections

from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

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


def get_all_related_perimeter_ids(search_perimeter_id):
    """Return a list of all perimeter ids related to the searched perimeter.

    When we filter by a given perimeter, we must return all aids:
        - where the perimeter is wider and contains the searched perimeter ;
        - where the perimeter is smaller and contained by the searched
        perimeter ;

    E.g if we search for aids in "Hérault (department), we must display all
    aids that are applicable to:

        - Hérault ;
        - Occitanie ;
        - France ;
        - Europe ;
        - M3M (and all other epcis in Hérault) ;
        - Montpellier (and all other communes in Hérault) ;
    """

    # Note: the original way we adressed this was more straightforward,
    # but we got very very bad perf results (like, queries with very slow
    # execution times > 30s).
    # Thus, we had to "help" Postgres' execution planner a little.

    # We just need to efficiently get a list of all perimeter ids related
    # to the current query.

    Through = Perimeter.contained_in.through
    contains_id = Through.objects \
        .filter(from_perimeter_id=search_perimeter_id) \
        .values('to_perimeter_id') \
        .distinct()
    contained_id = Through.objects \
        .filter(to_perimeter_id=search_perimeter_id) \
        .values('from_perimeter_id') \
        .distinct()

    q_exact_match = Q(id=search_perimeter_id)
    q_contains = Q(id__in=contains_id)
    q_contained = Q(id__in=contained_id)

    perimeter_qs = Perimeter.objects \
        .filter(q_exact_match | q_contains | q_contained) \
        .values('id') \
        .distinct()
    return perimeter_qs


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
    duplicates = [item for item, count in
                  collections.Counter(item_list).items() if count > 1]
    if len(duplicates):
        msg = _('This file is valid, but contains \
                duplicates: {}').format(duplicates)
        raise Exception(msg)

    return item_list


def query_cities_from_list(city_codes_list):
    return Perimeter.objects \
        .filter(code__in=city_codes_list) \
        .filter(scale=Perimeter.SCALES.commune)


def query_epcis_from_list(epci_names_list):
    return Perimeter.objects \
        .filter(name__in=epci_names_list) \
        .filter(scale=Perimeter.SCALES.epci)


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
    SCALES_LIST = [key for (key, value) in Perimeter.SCALES]

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
            if container != adhoc and SCALES_LIST.index(container.scale) <= SCALES_LIST.index(Perimeter.SCALES.adhoc):  # noqa
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
    in_city_codes = Perimeter.objects \
        .filter(scale=Perimeter.SCALES.commune) \
        .filter(contained_in__in=add_perimeters) \
        .values_list('code', flat=True)

    out_city_codes = Perimeter.objects \
        .filter(scale=Perimeter.SCALES.commune) \
        .filter(contained_in__in=rm_perimeters) \
        .values_list('code', flat=True)

    return set(in_city_codes) - set(out_city_codes)
