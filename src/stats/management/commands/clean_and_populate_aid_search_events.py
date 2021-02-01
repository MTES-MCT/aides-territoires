# flake8: noqa
from django.core.management.base import BaseCommand

from stats.models import AidSearchEvent


class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        self.stdout.write('Cleaning & populating fields of new Aid Search Events')

        events_to_populate = AidSearchEvent.objects.filter(fields_populated=False)
        self.stdout.write('About to process {} events...'.format(len(events_to_populate)))
        for event in events_to_populate:
            event.clean_and_populate_search_fields()

        self.stdout.write('Done !')
