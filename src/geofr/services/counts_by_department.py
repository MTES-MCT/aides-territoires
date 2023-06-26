from django.db.models import Count
from aids.constants import FINANCIAL_AIDS_LIST, TECHNICAL_AIDS_LIST
from aids.models import Aid
from geofr.models import Perimeter
from geofr.utils import get_all_related_perimeters

from django.db.models.query import QuerySet
from django.db.models import Q
from backers.models import Backer
from programs.models import Program
from categories.models import Category
from projects.models import ValidatedProject


def get_projects_count_by_department(
    dep_id: str,
) -> QuerySet:
    """
    For a given department, returns a list of projects
    """
    related_perimeters = get_all_related_perimeters(dep_id, values=["id"])

    validated_projects = ValidatedProject.objects.prefetch_related(
        "organization__perimeter"
    )
    validated_projects = validated_projects.filter(
        organization__perimeter_id__in=related_perimeters,
    )

    return validated_projects.count()


def get_backers_count_by_department(
    dep_id: str,
    target_audience: str = None,
    aid_type: str = None,
    perimeter_scale: str = None,
    backer_category: str = None,
) -> QuerySet:
    """
    For a given department, returns a list of backers with the number of associated live aids
    """
    related_perimeters = get_all_related_perimeters(dep_id, values=["id"])
    live_aids = Aid.objects.live()

    backers = Backer.objects.prefetch_related("financed_aids").select_related(
        "perimeter", "group__subcategory__category"
    )

    if target_audience:
        backers = backers.filter(
            financed_aids__targeted_audiences__overlap=[target_audience],
        )

    if backer_category and backer_category != "":
        backers = backers.filter(
            financed_aids__perimeter_id__in=related_perimeters,
            group__subcategory__category=backer_category,
        )

    if backer_category and backer_category != "":
        backers = backers.filter(
            perimeter_id__in=related_perimeters,
            financed_aids__in=live_aids,
            financed_aids__perimeter_id__in=related_perimeters,
            backer_group__subcategory__category=backer_category,
        )
    else:
        backers = backers.filter(
            financed_aids__in=live_aids,
            financed_aids__perimeter_id__in=related_perimeters,
            perimeter_id__in=related_perimeters,
        )

    if perimeter_scale == "local_group":
        backers = backers.filter(
            perimeter__scale__in=[
                Perimeter.SCALES.commune,
                Perimeter.SCALES.epci,
                Perimeter.SCALES.department,
                Perimeter.SCALES.region,
                Perimeter.SCALES.adhoc,
                Perimeter.SCALES.basin,
                Perimeter.SCALES.overseas,
            ],
        )
    elif perimeter_scale == "national_group":
        backers = backers.filter(
            perimeter__scale__in=[
                Perimeter.SCALES.mainland,
                Perimeter.SCALES.country,
                Perimeter.SCALES.continent,
            ],
        )

    backers = backers.filter(
        perimeter_id__in=related_perimeters,
        financed_aids__in=live_aids,
        financed_aids__perimeter_id__in=related_perimeters,
    )

    if aid_type == "financial_group":
        backers = (
            backers.distinct()
            .annotate(
                financial_aids=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=FINANCIAL_AIDS_LIST)),
                    distinct=True,
                )
            )
            .filter(financial_aids__gte=1)
            .annotate(
                grant_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=["grant"])),
                    distinct=True,
                )
            )
            .annotate(
                loan_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=["loan"])),
                    distinct=True,
                )
            )
            .annotate(
                recoverable_advance_count=Count(
                    "financed_aids",
                    filter=(
                        Q(financed_aids__aid_types__overlap=["recoverable_advance"])
                    ),
                    distinct=True,
                )
            )
            .annotate(
                cee_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=["cee"])),
                    distinct=True,
                )
            )
            .annotate(
                other_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=["other"])),
                    distinct=True,
                )
            )
            .values(
                "name",
                "id",
                "slug",
                "perimeter__name",
                "perimeter__scale",
                "group__subcategory__category__name",
                "financial_aids",
                "grant_count",
                "loan_count",
                "recoverable_advance_count",
                "cee_count",
                "other_count",
            )
            .order_by("-financial_aids")
        )
    elif aid_type == "technical_group":
        backers = (
            backers.distinct()
            .annotate(
                technical_aids=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=TECHNICAL_AIDS_LIST)),
                    distinct=True,
                )
            )
            .filter(technical_aids__gte=1)
            .annotate(
                technical_count=Count(
                    "financed_aids",
                    filter=(
                        Q(financed_aids__aid_types__overlap=["technical_engineering"])
                    ),
                    distinct=True,
                )
            )
            .annotate(
                financial_count=Count(
                    "financed_aids",
                    filter=(
                        Q(financed_aids__aid_types__overlap=["financial_engineering"])
                    ),
                    distinct=True,
                )
            )
            .annotate(
                legal_count=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=["legal_engineering"])),
                    distinct=True,
                )
            )
            .values(
                "name",
                "id",
                "slug",
                "perimeter__name",
                "perimeter__scale",
                "group__subcategory__category__name",
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
            .annotate(
                total_aids=Count(
                    "financed_aids",
                    distinct=True,
                )
            )
            .annotate(
                technical_aids=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=TECHNICAL_AIDS_LIST)),
                    distinct=True,
                )
            )
            .annotate(
                financial_aids=Count(
                    "financed_aids",
                    filter=(Q(financed_aids__aid_types__overlap=FINANCIAL_AIDS_LIST)),
                    distinct=True,
                )
            )
            .values(
                "name",
                "id",
                "slug",
                "perimeter__name",
                "perimeter__scale",
                "group__subcategory__category__name",
                "total_aids",
                "technical_aids",
                "financial_aids",
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
    related_perimeters = get_all_related_perimeters(dep_id, values=["id"])
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

    if aid_type == "financial_group":
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
                    filter=(Q(aids__aid_types__overlap=["grant"])),
                )
            )
            .annotate(
                loan_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__overlap=["loan"])),
                )
            )
            .annotate(
                recoverable_advance_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__overlap=["recoverable_advance"])),
                )
            )
            .annotate(
                cee_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__overlap=["cee"])),
                )
            )
            .annotate(
                other_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__overlap=["other"])),
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
                "cee_count",
                "other_count",
            )
            .order_by("-financial_aids")
        )
    elif aid_type == "technical_group":
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
                    filter=(Q(aids__aid_types__overlap=["technical_engineering"])),
                )
            )
            .annotate(
                financial_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__overlap=["financial_engineering"])),
                )
            )
            .annotate(
                legal_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__overlap=["legal_engineering"])),
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
    related_perimeters = get_all_related_perimeters(dep_id, values=["id"])
    return (
        Aid.objects.live()
        .filter(perimeter_id__in=related_perimeters)
        .distinct()
        .count()
    )


def get_categories_total_by_department(dep_id: str) -> int:
    """
    For a given department, returns the number of categories
    """
    related_perimeters = get_all_related_perimeters(dep_id, values=["id"])
    live_aids = Aid.objects.live()
    return (
        Category.objects.prefetch_related("aids")
        .filter(aids__in=live_aids, aids__perimeter_id__in=related_perimeters)
        .distinct()
        .count()
    )
