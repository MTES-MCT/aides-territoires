from django.utils import timezone
from django.db.models import Count
from aids.models import Aid, AidWorkflow
from geofr.utils import get_all_related_perimeter_ids
from aids.utils import filter_generic_aids

from django.db.models.query import QuerySet
from django.db.models import Q
from backers.models import Backer


def get_backers_count_by_departement(dep_id: str, detailed: bool = False) -> QuerySet:
    """
    For a given departement, returns a list of backers with  the number of aids
    """
    related_perimeters = get_all_related_perimeter_ids(dep_id)

    today = timezone.now().date()

    backers = (
        Backer.objects.prefetch_related("financed_aids")
        .filter(
            (
                Q(financed_aids__submission_deadline__gte=today)
                | Q(financed_aids__submission_deadline__isnull=True)
                | Q(financed_aids__recurrence="ongoing")
            ),
            financed_aids__perimeter_id__in=related_perimeters,
            financed_aids__status=AidWorkflow.states.published,
        )
        .annotate(total_aids=Count("financed_aids"))
        .annotate(
            technical_aids=Count(
                "financed_aids",
                filter=(
                    Q(financed_aids__aid_types=["technical"])
                    | Q(financed_aids__aid_types=["financial"])
                    | Q(financed_aids__aid_types=["legal"])
                ),
            )
        )
        .annotate(
            financial_aids=Count(
                "financed_aids",
                filter=(
                    Q(financed_aids__aid_types=["grant"])
                    | Q(financed_aids__aid_types=["loan"])
                    | Q(financed_aids__aid_types=["recoverable_advance"])
                    | Q(financed_aids__aid_types=["other"])
                ),
            )
        )
        .values("name", "id", "slug", "total_aids", "technical_aids", "financial_aids")
        .order_by("-total_aids")
    )

    return backers
