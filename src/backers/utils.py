from django.db.models import Count
from aids.constants import FINANCIAL_AIDS_LIST, TECHNICAL_AIDS_LIST
from aids.models import Aid
from geofr.utils import get_all_related_perimeter_ids

from django.db.models.query import QuerySet
from django.db.models import Q
from backers.models import Backer
from programs.models import Program


def get_backers_count_by_departement(dep_id: str) -> QuerySet:
    """
    For a given departement, returns a list of backers with  the number of associated live aids
    """
    related_perimeters = get_all_related_perimeter_ids(dep_id)
    live_aids = Aid.objects.live()

    backers = (
        Backer.objects.prefetch_related("financed_aids")
        .filter(
            financed_aids__in=live_aids,
            financed_aids__perimeter_id__in=related_perimeters,
        )
        .annotate(total_aids=Count("financed_aids"))
        .annotate(
            technical_aids=Count(
                "financed_aids",
                filter=(Q(financed_aids__aid_types__overlap=TECHNICAL_AIDS_LIST)),
            )
        )
        .annotate(
            financial_aids=Count(
                "financed_aids",
                filter=(Q(financed_aids__aid_types__overlap=FINANCIAL_AIDS_LIST)),
            )
        )
        .values("name", "id", "slug", "total_aids", "technical_aids", "financial_aids")
        .order_by("-total_aids")
    )

    return backers

def get_programs_count_by_departement(dep_id: str) -> QuerySet:
    """
    For a given departement, returns a list of programs with the number of associated live aids
    """
    related_perimeters = get_all_related_perimeter_ids(dep_id)
    live_aids = Aid.objects.live()

    programs = (
        Program.objects.prefetch_related("aids")
        .filter(
            aids__in=live_aids,
            aids__perimeter_id__in=related_perimeters,
        )
        .annotate(total_aids=Count("aids"))
        .annotate(
            technical_aids=Count(
                "aids",
                filter=(Q(aids__aid_types__overlap=TECHNICAL_AIDS_LIST)),
            )
        )
        .annotate(
            financial_aids=Count(
                "aids",
                filter=(Q(aids__aid_types__overlap=FINANCIAL_AIDS_LIST)),
            )
        )
        .values("name", "id", "slug", "total_aids", "technical_aids", "financial_aids")
        .order_by("-total_aids")
    )

    return programs