from django.core.management.base import BaseCommand

from map.utils import get_backers_count_by_department, get_programs_count_by_department
from geofr.models import Perimeter


class Command(BaseCommand):
    """For every French department, check how many backers and programs have live aids"""

    def handle(self, *args, **options):

        departments = Perimeter.objects.filter(
            scale=Perimeter.SCALES.department)
        for department in departments:
            department.backers_count = get_backers_count_by_department(department.id).count()
            department.programs_count = get_programs_count_by_department(department.id).count()
            department.save()
