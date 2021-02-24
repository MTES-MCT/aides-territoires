from core.celery import app
from core.utils import get_subdomain_from_host
from search.utils import clean_search_querystring
from stats.models import AidViewEvent, Event


@app.task
def log_aidviewevent(aid_id, querystring='', source=''):
    source_cleaned = get_subdomain_from_host(source)
    querystring_cleaned = clean_search_querystring(querystring)

    AidViewEvent.objects.create(
            aid_id=aid_id,
            querystring=querystring_cleaned,
            source=source_cleaned)


def log_event(category, event, meta='', source='', value=None):
    Event.objects.create(
        category=category,
        event=event,
        meta=meta,
        source=source,
        value=value)
