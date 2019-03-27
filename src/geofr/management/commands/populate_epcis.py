import json
from unipath import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_DEPARTMENTS, DEPARTMENT_TO_REGION


DATA_FILE = '@etalab/epci/data/epci.json'


class Command(BaseCommand):
    """Import the list of all epcis.

    This task is highly inefficient (no batch saving, updating every row one by
    one, etc.) but it will be ran once per year, so it's not a big deal.

    We use epci data as provided by the geo api npm package.

    Make sure you install js dev dependencies before running this task.
    """
    def handle(self, *args, **options):
        node_modules_path = settings.NODE_MODULES_PATH
        data_file_path = Path(node_modules_path, Path(DATA_FILE))

        if not data_file_path.exists():
            self.stdout.write(self.style.ERROR('File does not exist'))

        with open(data_file_path, 'r') as fp:
            json_data = json.load(fp)

        for epci_data in json_data:
            self.import_epci(epci_data)

    def import_epci(self, data):
        """Process a single EPCI data.

        We must update the epci itself, then update it's members.
        """
        member_codes = [m['code'] for m in data['membres']]
        members = Perimeter.objects.filter(code__in=member_codes)
        member_depts = []
        for member in members:
            member_depts += member.departments
        unique_depts = list(set(member_depts))
        regions = [DEPARTMENT_TO_REGION[dept] for dept in unique_depts]
        unique_regions = list(set(regions))
        is_overseas = bool(unique_depts[0] in OVERSEAS_DEPARTMENTS)

        epci_name = data['nom']
        epci_code = data['code']
        epci, created = Perimeter.objects.update_or_create(
            scale=Perimeter.TYPES.epci,
            code=epci_code,
            defaults={
                'name': epci_name,
                'departments': unique_depts,
                'regions': unique_regions,
                'is_overseas': is_overseas
            })
        members.update(epci=epci_code)

        if created:
            self.stdout.write('New EPCI {}'.format(epci_name))
