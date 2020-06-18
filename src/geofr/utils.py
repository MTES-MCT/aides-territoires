from django.db import transaction
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
    perimeters = Perimeter.objects \
        .filter(code__in=city_codes) \
        .filter(scale=Perimeter.TYPES.commune) \
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
    in_city_codes = Perimeter.objects \
        .filter(scale=Perimeter.TYPES.commune) \
        .filter(contained_in__in=add_perimeters) \
        .values_list('code', flat=True)

    out_city_codes = Perimeter.objects \
        .filter(scale=Perimeter.TYPES.commune) \
        .filter(contained_in__in=rm_perimeters) \
        .values_list('code', flat=True)

    return set(in_city_codes) - set(out_city_codes)
