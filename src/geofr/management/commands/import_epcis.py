import os

import xlrd
from django.core.management.base import BaseCommand

from geofr.models import Perimeter
from geofr.constants import OVERSEAS_DEPARTMENTS, DEPARTMENT_TO_REGION


# Field column indexes
NAME = 2
DEPARTMENT = 0
CODE = 1
MEMBER = 9


class Command(BaseCommand):
    """Import the list of all epcis.

    This task is highly inefficient (no batch saving, updating every row one by
    one, etc.) but it will be ran only once, so it's not a big deal.

    The file can be downloaded at this address:
    https://www.collectivites-locales.gouv.fr/liste-et-composition-2018
    """

    def add_arguments(self, parser):
        parser.add_argument('epci_file', nargs=1, type=str)

    def handle(self, *args, **options):

        xls_book = xlrd.open_workbook(os.path.abspath(options['epci_file'][0]))
        self.xls_sheet = xls_book.sheet_by_index(0)

        for row_index in range(1, self.xls_sheet.nrows):
            self.import_epci_member(row_index)

    def import_epci_member(self, row_index):
        """Process a single line in the file.

        Every line describes one member (e.g a commune) for one EPCI.

        Hence, EPCI description is duplicated in several lines.

        """
        epci_name = self.xls_sheet.cell_value(row_index, NAME)
        epci_department = self.xls_sheet.cell_value(row_index, DEPARTMENT)
        epci_region = DEPARTMENT_TO_REGION[epci_department]
        epci_code = '{:d}'.format(
            int(self.xls_sheet.cell_value(row_index, CODE)))
        member_code = self.xls_sheet.cell_value(row_index, MEMBER)

        epci, created = Perimeter.objects.get_or_create(
            scale=Perimeter.TYPES.epci,
            code=epci_code,
            name=epci_name,
            departments=[epci_department],
            regions=[epci_region],
            is_overseas=bool(epci_department in OVERSEAS_DEPARTMENTS))

        epci.save()

        Perimeter.objects.filter(code=member_code).update(epci=epci_code)

        if created:
            self.stdout.write('New EPCI {}'.format(epci_name))
