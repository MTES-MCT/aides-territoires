import logging

from core.celery import app
from stats.utils import log_event
from aids.models import Aid
from search.models import SearchPage


logger = logging.getLogger(__name__)


@app.task
def store_aids_live_count():
    logger.info("Starting stats 'aid live count' task")
    # main website
    aids_live_count = Aid.objects.live().count()
    log_event(
        "aid", "live_count", source="aides-territoires", value=aids_live_count
    )  # noqa
    # all PP
    for search_page in SearchPage.objects.all():
        search_page_aids_live_count = search_page.get_base_queryset().count()
        log_event(
            "aid",
            "live_count",
            source=search_page.slug,
            value=search_page_aids_live_count,
        )  # noqa
