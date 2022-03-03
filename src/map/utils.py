from django.db.models import Count
from aids.constants import FINANCIAL_AIDS_LIST, TECHNICAL_AIDS_LIST
from aids.models import Aid
from geofr.utils import get_all_related_perimeter_ids

from django.db.models.query import QuerySet
from django.db.models import Q
from backers.models import Backer
from programs.models import Program


def get_backers_count_by_department(dep_id: str, target_audience: str = None, aid_type: str = None) -> QuerySet:
    """
    For a given department, returns a list of backers with  the number of associated live aids
    """
    related_perimeters = get_all_related_perimeter_ids(dep_id)
    live_aids = Aid.objects.live()

    backers = Backer.objects.prefetch_related("financed_aids")

    if target_audience:
        backers = (
            backers.filter(
                financed_aids__in=live_aids,
                financed_aids__perimeter_id__in=related_perimeters,
                financed_aids__targeted_audiences__overlap=[target_audience]            )
        )
    else:
        backers = (
            backers.filter(
                financed_aids__in=live_aids,
                financed_aids__perimeter_id__in=related_perimeters,
            )
        )

    if aid_type == "financial":
        backers = (
            backers.distinct()
            .annotate(
                grant=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["grant"])),
                )
            )
            .annotate(
                loan=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["loan"])),
                )
            )
            .annotate(
                recoverable_advance=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["recoverable_advance"])),
                )
            )
            .annotate(
                other=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["other"])),
                )
            )
            .values("name", "id", "slug", "grant", "loan", "recoverable_advance", "other")
            .order_by("-grant")
        )
    elif aid_type == "technical":
        backers = (
            backers.distinct()
            .annotate(
                technical=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["technical"])),
                )
            )
            .annotate(
                financial=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["financial"])),
                )
            )
            .annotate(
                legal=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["legal"])),
                )
            )
            .values("name", "id", "slug", "technical", "financial", "legal")
            .order_by("-technical")
        )
 
    else:
        backers = (
            backers.distinct()
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

def get_programs_count_by_department(dep_id: str, target_audience: str = None, aid_type: str = None) -> QuerySet:
    """
    For a given department, returns a list of programs with the number of associated live aids
    """
    related_perimeters = get_all_related_perimeter_ids(dep_id)
    live_aids = Aid.objects.live()

    programs = Program.objects.prefetch_related("aids")

    if target_audience:
        programs = programs.filter(
            aids__in=live_aids,
            aids__perimeter_id__in=related_perimeters,
            aids__targeted_audiences__overlap=[target_audience]
        )
    else:
        programs = programs.filter(
            aids__in=live_aids,
            aids__perimeter_id__in=related_perimeters,
        )

    if aid_type == "financial":
        programs = (
            programs
            .annotate(total_aids=Count("aids"))
            .annotate(
                grant=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["grant"])),
                )
            )
            .annotate(
                loan=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["loan"])),
                )
            )
            .annotate(
                recoverable_advance=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["recoverable_advance"])),
                )
            )
            .annotate(
                other=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["other"])),
                )
            )
            .values("name", "id", "slug", "grant", "loan", "recoverable_advance", "other")
            .order_by("-grant")
        )
    elif aid_type == "technical":
        programs = (
            programs
            .annotate(total_aids=Count("aids"))
            .annotate(
                technical=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["technical"])),
                )
            )
            .annotate(
                financial=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["financial"])),
                )
            )
            .annotate(
                recoverable_advance=Count(
                    "legal",
                    filter=(Q(aids__aid_types__contains=["legal"])),
                )
            )
            .values("name", "id", "slug", "technical", "financial", "legal")
            .order_by("-technical")
        )
    else:
        programs = (
            programs
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