import logging

from core.celery import app
from stats.utils import log_event
from aids.models import Aid


logger = logging.getLogger(__name__)


@app.task
def store_aids_live_count():
    logger.info("Starting stats 'aid live count' task")
    aids_live_count = Aid.objects.live().count()
    log_event('aid', 'live_count', source='aides-territoires', value=aids_live_count)  # noqa
