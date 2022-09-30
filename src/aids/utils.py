import re

from django.utils import timezone
from django.db.models.query import QuerySet

from geofr.models import Perimeter

# The regex to detect existing title prefixes for duplicate aids
CLONE_PREFIX_RE = r"^\[Copie( \d{2}h\d{2})?\] "
#                   ^                           | Starts with...
#                    \[Copie               \]   | the string "[Copie] "...
#                           (            )?     | containing an optional...
#                             \d{2}h\d{2}       | H:M timestamp


def generate_clone_title(aid_title, now=None):
    """Return a suitable name for a duplicate aid.

    >>> generate_clone_name('Aid title')
    [Copie 10h04] Aid title]

    >>> generate_clone_name('[Copie 10h04] Aid title')
    [Copie 10h05] Aid title]
    """
    now = now or timezone.now()

    title_without_prefix = re.sub(CLONE_PREFIX_RE, r"", aid_title)
    new_title = f"[Copie {now:%Hh%M}] {title_without_prefix}"
    return new_title


def filter_generic_aids(qs: QuerySet, search_perimeter: Perimeter = None) -> QuerySet:
    """
    We should never have both the generic aid and its local version
    together on search results.
    Which one should be removed from the result ? It depends...
    We consider the scale perimeter associated to the local aid.
    - When searching on a wider area than the local aid's perimeter,
        then we display the generic version.
    - When searching on a smaller area than the local aid's perimeter,
        then we display the local version.
    """

    # We will consider local aids for which the associated generic
    # aid is listed in the results - We should consider excluding a
    # local aid, only when it's generic aid is listed.
    generic_aids = qs.generic_aids()
    local_aids = qs.local_aids().filter(generic_aid__in=generic_aids)
    # We use a python list for better performance
    local_aids_list = local_aids.values_list(
        "pk", "perimeter__scale", "generic_aid__pk"
    )
    aids_to_exclude = []
    if not search_perimeter:
        # If the user does not specify a search perimeter, then we go wide.
        search_smaller = False
        search_wider = True
    for aid_id, perimeter_scale, generic_aid_id in local_aids_list:
        if search_perimeter:
            search_smaller = search_perimeter.scale <= perimeter_scale
            search_wider = search_perimeter.scale > perimeter_scale
        # If the search perimeter is smaller or matches exactly the local
        # perimeter, then it's relevant to keep the local and exclude
        # the generic aid.Excluding the generic aid takes precedence
        # over excluding the local aid.
        if search_smaller:
            aids_to_exclude.append(generic_aid_id)
        elif search_wider:
            # If the search perimeter is wider than the local perimeter
            # then it more relevant to keep the generic aid and exclude the
            # the local one.
            aids_to_exclude.append(aid_id)
    qs = qs.exclude(pk__in=aids_to_exclude)
    return qs
