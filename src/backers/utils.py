from django.utils import timezone
from django.db.models import Count
from aids.constants import FINANCIAL_AIDS_LIST, TECHNICAL_AIDS_LIST
from aids.models import AidWorkflow
from geofr.utils import get_all_related_perimeter_ids

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
