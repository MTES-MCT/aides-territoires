from stats.models import Event


def log_event(category, event, meta='', value=None):
    Event.objects.create(
        category=category,
        event=event,
        meta=meta,
        value=value)
