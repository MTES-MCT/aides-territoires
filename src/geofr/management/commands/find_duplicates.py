from django.core.management.base import BaseCommand

from geofr.models import Perimeter

class Command(BaseCommand):
    help = "Find ad-hoc perimeters that cover the same places"


    def handle(self, *args, **options):
        # Get all the adhoc perimeters relations
        adhoc_contains = Perimeter.objects.filter(scale=18).values_list("id", "contains")

        # Group them by perimeter
        adhoc_perimeters_dict = {}
        for i in adhoc_contains:
            adhoc_perimeter = i[0]
            included_perimeter = i[1]
            if included_perimeter is not None:
                if adhoc_perimeter not in adhoc_perimeters_dict:
                    adhoc_perimeters_dict[adhoc_perimeter] = [included_perimeter]
                else:
                    adhoc_perimeters_dict[adhoc_perimeter].append(included_perimeter)

        # Now sorting the included perimeters
        for key, value in adhoc_perimeters_dict.items():
            adhoc_perimeters_dict[key] = sorted(value)

        duplicates = []
        for key1, value1 in adhoc_perimeters_dict.items():
            for key2, value2 in adhoc_perimeters_dict.items():
                if value1 == value2 and key1 > key2:
                    duplicates.append("{key1} is a duplicate of {key2}")

        print(f"{len(duplicates)} duplicates found.")
        for d in duplicates:
            print(d)
