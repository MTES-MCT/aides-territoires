import operator
from functools import reduce

from django.db.models import Q, Count
from django.db.models.query import QuerySet
from django.contrib.postgres.aggregates import ArrayAgg
from aids.constants import FINANCIAL_AIDS_LIST, TECHNICAL_AIDS_LIST
from aids.models import Aid
from geofr.models import Perimeter
from geofr.utils import get_all_related_perimeters

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
    target_audience: str | None = None,
    aid_type: str | None = None,
    perimeter_scale: str | None = None,
    backer_category: str | None = None,
    aid_category: str | None = None,
) -> QuerySet:
    """
    For a given department, returns a list of backers with the number of associated live aids
    """
    related_perimeters = get_all_related_perimeters(dep_id, values=["id"])
    live_aids = Aid.objects.live()

    backers = Backer.objects.prefetch_related("financed_aids").select_related(
        "perimeter"
    )

    q_filters = []

    perimeter_id_in_filter = Q(perimeter_id__in=related_perimeters)
    q_filters.append(perimeter_id_in_filter)

    financed_aids__in_filter = Q(financed_aids__in=live_aids)
    q_filters.append(financed_aids__in_filter)

    financed_aids__perimeter_id__in_filter = Q(
        financed_aids__perimeter_id__in=related_perimeters
    )
    q_filters.append(financed_aids__perimeter_id__in_filter)

    if target_audience:
        target_audience_filter = Q(
            financed_aids__targeted_audiences__overlap=[target_audience],
        )
        q_filters.append(target_audience_filter)

    if backer_category and backer_category != "":
        backer_category_filter = Q(
            group__subcategory__category=backer_category,
        )
        q_filters.append(backer_category_filter)

    if aid_category and aid_category != "":
        aid_categories = aid_category.split(",")
        aid_categories_filter = Q(
            financed_aids__categories__slug__in=aid_categories,
        )
        q_filters.append(aid_categories_filter)

    if perimeter_scale == "local_group":
        perimeter_scale_filter = Q(
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
        q_filters.append(perimeter_scale_filter)
    elif perimeter_scale == "national_group":
        perimeter_scale_filter = Q(
            perimeter__scale__in=[
                Perimeter.SCALES.mainland,
                Perimeter.SCALES.country,
                Perimeter.SCALES.continent,
            ],
        )
        q_filters.append(perimeter_scale_filter)

    if q_filters:
        backers = backers.filter(reduce(operator.and_, q_filters))

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
            .annotate(
                aids_categories=ArrayAgg(
                    "financed_aids__categories__theme__name", distinct=True
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
                "aids_categories",
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
                        Q(
                            financed_aids__aid_types__overlap=[
                                "strategic_engineering",
                                "diagnostic_engineering",
                                "animation_engineering",
                                "AMOA_engineering",
                                "MOE_engineering",
                            ]
                        )
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
                    filter=(
                        Q(
                            financed_aids__aid_types__overlap=[
                                "administrative_engineering",
                                "legal_and_regulatory_engineering",
                            ]
                        )
                    ),
                    distinct=True,
                )
            )
            .annotate(
                formation_count=Count(
                    "financed_aids",
                    filter=(
                        Q(financed_aids__aid_types__overlap=["formation_engineering"])
                    ),
                    distinct=True,
                )
            )
            .annotate(
                aids_categories=ArrayAgg(
                    "financed_aids__categories__theme__name", distinct=True
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
                "formation_count",
                "aids_categories",
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
            .annotate(
                aids_categories=ArrayAgg(
                    "financed_aids__categories__theme__name", distinct=True
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
                "aids_categories",
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
                    filter=(
                        Q(
                            aids__aid_types__overlap=[
                                "strategic_engineering",
                                "diagnostic_engineering",
                                "animation_engineering",
                                "AMOA_engineering",
                                "MOE_engineering",
                            ]
                        )
                    ),
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
                    filter=(
                        Q(
                            aids__aid_types__overlap=[
                                "administrative_engineering",
                                "legal_and_regulatory_engineering",
                            ]
                        )
                    ),
                )
            )
            .annotate(
                formation_count=Count(
                    "aids",
                    filter=(Q(aids__aid_types__overlap=["formation_engineering"])),
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
                "formation_count",
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
