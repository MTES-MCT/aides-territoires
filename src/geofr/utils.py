import collections
import logging

from django.db import transaction
from django.db.models import Q
from django.core.files.uploadedfile import InMemoryUploadedFile

from geofr.constants import OVERSEAS_PREFIX, DEPARTMENT_TO_REGION
from geofr.models import Perimeter, PerimeterImport
from accounts.models import User

MAX_PERIMETERS_TO_ATTACH = 7000


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


def get_all_related_perimeters(
    search_perimeter_id, direction="both", scale=None, values=None
):
    """Return a list of all perimeters related to the searched perimeter.

    In case of direction `up`, we only retrieve the wider perimeters.
    In case of direction `down`, we only retrieve the smaller perimeters.

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

    The `scale` parameter allows you to restrict results to a given
    `Perimeter.SCALES` kind of perimeter.

    The `values` list parameter allows you to return values instead of
    instances of Perimeters.
    """

    # Note: the original way we adressed this was more straightforward,
    # but we got very very bad perf results (like, queries with very slow
    # execution times > 30s).
    # Thus, we had to "help" Postgres' execution planner a little.

    # We just need to efficiently get a list of all perimeter ids related
    # to the current query.
    q_exact_match = Q(id=search_perimeter_id)

    Through = Perimeter.contained_in.through
    q_contains = Q()
    q_contained = Q()
    if direction == "both" or direction == "up":
        contains_id = (
            Through.objects.filter(from_perimeter_id=search_perimeter_id)
            .values("to_perimeter_id")
            .distinct()
        )
        q_contains = Q(id__in=contains_id)
    if direction == "both" or direction == "down":
        contained_id = (
            Through.objects.filter(to_perimeter_id=search_perimeter_id)
            .values("from_perimeter_id")
            .distinct()
        )
        q_contained = Q(id__in=contained_id)

    perimeter_qs = Perimeter.objects.filter(q_exact_match | q_contains | q_contained)
    if scale is not None:
        perimeter_qs = perimeter_qs.filter(scale=scale)
    if values is not None:
        perimeter_qs = perimeter_qs.values(*values)
    return perimeter_qs.distinct()


def extract_perimeters_from_file(perimeter_list_file: InMemoryUploadedFile) -> list:
    """
    Extracts a list of either:
    - Commune Insee codes
    - EPCI names
    - EPCI Siren codes
    from an imported file
    """
    item_list = []

    # extract items
    for line in perimeter_list_file:
        try:
            item = line.decode().strip().split(";")[0]
            clean_item = str(item.strip('"').strip("'"))
            if clean_item:  # ignore empty lines
                item_list.append(clean_item)
        except (UnicodeDecodeError, ValueError) as e:
            msg = f"""
            Ce fichier semble invalide ; merci de vérifier son contenu. Si vous pensez
            qu’il s'agit d’une erreur, contactez l’équipe de développement. Voici "
            l’erreur d'origine : {e}"""
            raise Exception(msg)

    # check for duplicates
    duplicates = [
        item for item, count in collections.Counter(item_list).items() if count > 1
    ]
    if len(duplicates):
        msg = f"Ce fichier est valide, mais comporte des doublons: {duplicates}"
        raise Exception(msg)

    return item_list


def query_cities_from_list(city_codes_list):
    return Perimeter.objects.filter(code__in=city_codes_list).filter(
        scale=Perimeter.SCALES.commune
    )


def query_epcis_from_list(epci_list: list, data_type: str = "names"):
    qs = Perimeter.objects.filter(scale=Perimeter.SCALES.epci)

    if data_type == "names":
        qs = qs.filter(name__in=epci_list)
    elif data_type == "codes":
        qs = qs.filter(code__in=epci_list)

    return qs


def attach_epci_perimeters(
    adhoc: Perimeter, epci_list: list, user: User, data_type: str
) -> dict:
    """
    Attach EPCI Perimeters from either a list of EPCI names or EPCI
    codes, as stated by the value of data_type ("names" or "codes")
    """
    # first get the epci_query from the epci_list
    epci_query = query_epcis_from_list(epci_list, data_type)
    # get the city_codes list from these epci perimeters
    city_codes = combine_perimeters(epci_query, [])
    # finally call the usual attach_perimeters_check method
    result = attach_perimeters_check(adhoc, city_codes, user)
    return result


def attach_perimeters_check(
    adhoc: Perimeter, city_codes: list, user: User, logger=None
) -> dict:
    """
    Checks the numbers of city codes to import
    If it is too high, create PerimeterImport object
    Else run attach_perimeters function
    """

    if not logger:
        logger = logging.getLogger(__name__)

    logger.info(f"{len(city_codes)} city codes found")

    city_codes = list(city_codes)

    if len(city_codes) > MAX_PERIMETERS_TO_ATTACH:
        logger.debug("Creating PerimeterImport object")

        PerimeterImport.objects.create(
            adhoc_perimeter=adhoc, city_codes=city_codes, author=user
        )
        logger.debug("PerimeterImport object created")
        return {"method": "delayed import"}
    else:
        logger.debug("Calling attach_perimeters function")
        attach_perimeters(adhoc, city_codes, logger)
        return {"method": "direct import"}


@transaction.atomic
def attach_perimeters(adhoc, city_codes, logger=None):
    """Attach an ad-hoc perimeter to other perimeters.

    This function makes sure the `adhoc` perimeter is added to the
    `contained_in` list of all perimeters corresponding to the `city_codes`.

    E.g if we want to attach the "Communes littorales" Ad-hoc perimeter to the
    "Vic-la-Gardiole" city perimeter, we add "Communes littorales" to
    "Vic-la-Gardiole".contained_in, but also to "Herault".contained_in,
    "Occitanie".contained_in…
    """
    # Define logger
    if not logger:
        logger = logging.getLogger(__name__)

    # Delete existing links
    PerimeterContainedIn = Perimeter.contained_in.through
    PerimeterContainedIn.objects.filter(to_perimeter_id=adhoc.id).delete()

    # Fetch perimeters corresponding to the given city codes
    perimeters = query_cities_from_list(city_codes).prefetch_related("contained_in")

    logger.info(f"{perimeters.count()} perimeters found")

    # Put the adhoc perimeter in the cities `contained_in` lists
    containing = []
    count = 0
    for perimeter in perimeters:
        containing.append(
            PerimeterContainedIn(
                from_perimeter_id=perimeter.id, to_perimeter_id=adhoc.id
            )
        )

        # Perimeters that contain the cities must contain the adhoc perimeter
        # except for France and Europe.
        for container in perimeter.contained_in.all():
            if container != adhoc and container.scale <= Perimeter.SCALES.adhoc:
                containing.append(
                    PerimeterContainedIn(
                        from_perimeter_id=container.id, to_perimeter_id=adhoc.id
                    )
                )

        count += 1
        if not (count % 500):
            logger.info(f"{count} perimeters done")

    # Bulk create the links
    PerimeterContainedIn.objects.bulk_create(containing, ignore_conflicts=True)

    logger.info(
        f"""Import finished.
        {count} perimeters attached to Ad-hoc perimeter {adhoc.name} ({adhoc.id})"""
    )


def combine_perimeters(add_perimeters, rm_perimeters):
    """Combine perimeters to extract some city codes.

    Return the city codes that are in `add_perimeters` and not in
    `rm_perimeters`.
    """
    in_city_codes = (
        Perimeter.objects.filter(scale=Perimeter.SCALES.commune)
        .filter(contained_in__in=add_perimeters)
        .values_list("code", flat=True)
    )

    out_city_codes = (
        Perimeter.objects.filter(scale=Perimeter.SCALES.commune)
        .filter(contained_in__in=rm_perimeters)
        .values_list("code", flat=True)
    )

    return set(in_city_codes) - set(out_city_codes)
