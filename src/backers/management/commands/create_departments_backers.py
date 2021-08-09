from django.core.management.base import BaseCommand

from backers.models import Backer
from geofr.models import Perimeter


class Command(BaseCommand):
    """Create backers entries for every french departments."""

    def handle(self, *args, **options):
        confirm = input('This command is meant to run in production only '
                        'once.\nAre you sure you know what you\'re doing?\n')
        if confirm != 'yes':
            return

        departments = Perimeter.objects.filter(
            scale=Perimeter.SCALES.department)
        backers = []
        for department in departments:
            backers.append(Backer(
                name='{} (Département)'.format(department.name)))

        results = Backer.objects.bulk_create(backers)
        self.stdout.write(self.style.SUCCESS(
            '{} backers created'.format(len(results))
        ))
