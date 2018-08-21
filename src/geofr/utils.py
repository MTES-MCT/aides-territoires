from geofr.constants import OVERSEAS_PREFIX, DEPARTMENT_TO_REGION


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
