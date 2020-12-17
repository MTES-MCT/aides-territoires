from stats.models import Event


def log_event(category, event, meta='', source='', value=None):
    Event.objects.create(
        category=category,
        event=event,
        meta=meta,
        source=source,
        value=value)
