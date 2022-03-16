from django.db.models import Count
from aids.constants import FINANCIAL_AIDS_LIST, TECHNICAL_AIDS_LIST
from aids.models import Aid
from geofr.utils import get_all_related_perimeter_ids

from django.db.models.query import QuerySet
from django.db.models import Q
from backers.models import Backer
from programs.models import Program
from categories.models import Category


def get_backers_count_by_department(
    dep_id: str, target_audience: str = None, aid_type: str = None
) -> QuerySet:
    """
    For a given department, returns a list of backers with  the number of associated live aids
    """
    related_perimeters = get_all_related_perimeter_ids(dep_id)
    live_aids = Aid.objects.live()

    backers = Backer.objects.prefetch_related("financed_aids")

    if target_audience:
        backers = backers.filter(
            financed_aids__in=live_aids,
            financed_aids__perimeter_id__in=related_perimeters,
            financed_aids__targeted_audiences__overlap=[target_audience],
        )
    else:
        backers = backers.filter(
            financed_aids__in=live_aids,
            financed_aids__perimeter_id__in=related_perimeters,
        )

    if aid_type == "financial":
        backers = (
            backers.distinct()
            .annotate(
                financial_aids=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=FINANCIAL_AIDS_LIST)),
                )
            )
            .filter(financial_aids__gte=1)
            .annotate(
                grant_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["grant"])),
                )
            )
            .annotate(
                loan_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["loan"])),
                )
            )
            .annotate(
                recoverable_advance_count=Count(
                    "financed_aids",
                    filter=(
                        Q(financed_aids__aid_types__contains=["recoverable_advance"])
                    ),
                )
            )
            .annotate(
                other_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["other"])),
                )
            )
            .values(
                "name",
                "id",
                "slug",
                "financial_aids",
                "grant_count",
                "loan_count",
                "recoverable_advance_count",
                "other_count",
            )
            .order_by("-financial_aids")
        )
    elif aid_type == "technical":
        backers = (
            backers.distinct()
            .annotate(
                technical_aids=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=TECHNICAL_AIDS_LIST)),
                )
            )
            .filter(technical_aids__gte=1)
            .annotate(
                technical_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["technical"])),
                )
            )
            .annotate(
                financial_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["financial"])),
                )
            )
            .annotate(
                legal_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__contains=["legal"])),
                )
            )
            .values(
                "name",
                "id",
                "slug",
                "technical_aids",
                "technical_count",
                "financial_count",
                "legal_count",
            )
            .order_by("-technical_aids")
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
            .values(
                "name", "id", "slug", "total_aids", "technical_aids", "financial_aids"
            )
            .order_by("-total_aids")
        )

    return backers


def get_programs_count_by_department(
    dep_id: str, target_audience: str = None, aid_type: str = None
) -> QuerySet:
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
            aids__targeted_audiences__overlap=[target_audience],
        )
    else:
        programs = programs.filter(
            aids__in=live_aids,
            aids__perimeter_id__in=related_perimeters,
        )

    if aid_type == "financial":
        programs = (
            programs.annotate(
                financial_aids=Count(
                    "aids",
                    filter=(Q(aids__aid_types__overlap=FINANCIAL_AIDS_LIST)),
                )
            )
            .filter(financial_aids__gte=1)
            .annotate(
                grant_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["grant"])),
                )
            )
            .annotate(
                loan_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["loan"])),
                )
            )
            .annotate(
                recoverable_advance_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["recoverable_advance"])),
                )
            )
            .annotate(
                other_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["other"])),
                )
            )
            .values(
                "name",
                "id",
                "slug",
                "financial_aids",
                "grant_count",
                "loan_count",
                "recoverable_advance_count",
                "other_count",
            )
            .order_by("-financial_aids")
        )
    elif aid_type == "technical":
        programs = (
            programs.annotate(
                technical_aids=Count(
                    "aids",
                    filter=(Q(aids__aid_types__overlap=TECHNICAL_AIDS_LIST)),
                )
            )
            .filter(technical_aids__gte=1)
            .annotate(
                technical_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["technical"])),
                )
            )
            .annotate(
                financial_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["financial"])),
                )
            )
            .annotate(
                legal_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__contains=["legal"])),
                )
            )
            .values(
                "name",
                "id",
                "slug",
                "technical_aids",
                "technical_count",
                "financial_count",
                "legal_count",
            )
            .order_by("-technical_aids")
        )
    else:
        programs = (
            programs.annotate(total_aids=Count("aids"))
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
            .values(
                "name", "id", "slug", "total_aids", "technical_aids", "financial_aids"
            )
            .order_by("-total_aids")
        )

    return programs


def get_live_aids_total_by_department(dep_id: str) -> int:
    """
    For a given department, returns the number of live aids
    """
    related_perimeters = get_all_related_perimeter_ids(dep_id)
    return Aid.objects.live().filter(perimeter_id__in=related_perimeters).count()


def get_categories_total_by_department(dep_id: str) -> int:
    """
    For a given department, returns the number of categories
    """
    related_perimeters = get_all_related_perimeter_ids(dep_id)
    live_aids = Aid.objects.live()
    return (
        Category.objects.prefetch_related("aids")
        .filter(aids__in=live_aids, aids__perimeter_id__in=related_perimeters)
        .distinct()
        .count()
    )
