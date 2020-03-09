from stats.models import Event


def log_event(category, event, value):
    Event.objects.create(
        category=category,
        event=event,
        value=value)
