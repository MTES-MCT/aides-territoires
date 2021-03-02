# flake8: noqa

import os
import csv

from django.core.management.base import BaseCommand
from django.utils import timezone

from aids.models import Aid
from geofr.models import Perimeter
from geofr.utils import perimeters_to_dict_with_contained
from categories.models import Category


LOCAL_PERIMETERS = Perimeter.objects.exclude(scale__in=[Perimeter.TYPES.country, Perimeter.TYPES.continent])
CATEGORY_TRANSITION = Category.objects.get(name='Transition énergétique')

CSV_COLUMNS = [
    'code',
    'nb_live_aids',
    'nb_live_aids_type_technical',
    'nb_live_aids_type_financial',
    'nb_live_aids_type_legal',
    'nb_live_aids_category_transition',
    'nb_live_aids_local',
    'nb_live_aids_type_technical_local',
    'nb_live_aids_type_financial_local',
    'nb_live_aids_type_legal_local',
    'nb_live_aids_category_transition_local']


class Command(BaseCommand):
    """
    For each scale item (e.g. commune) in our database, we calculate
    the number of aids they can apply for
    (with timestamp because this number evolves over time)

    Usage:
    python manage.py generate_geo_aids_count
    python manage.py generate_geo_aids_count --scale 'epci'
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--scale",
            type=str,
            choices=['commune', 'epci', 'basin', 'region', 'department'],
            default='commune',
            help="Set the aggregation scale. Optional.",
        )

    def handle(self, *args, **options):
        # init
        SCALE_AIDS_FILE_NAME = options['scale'] + 's_aids_count_' + timezone.now().strftime('%Y%m%d')
        SCALE_AIDS_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../data/' + SCALE_AIDS_FILE_NAME + '.csv'

        self.stdout.write('fetching live aids...')
        all_aids = Aid.objects \
            .select_related('perimeter') \
            .prefetch_related('categories') \
            .live()
        self.stdout.write(
            self.style.SUCCESS(f'{all_aids.count()} live aids'))

        self.stdout.write('generating perimeters_dict...')
        perimeters_dict = perimeters_to_dict_with_contained(scale=getattr(Perimeter.TYPES, options['scale']))
        self.stdout.write(
            self.style.SUCCESS(f'{len(perimeters_dict.keys())} perimeters'))

        self.stdout.write(f"generating {options['scale']} scale_code_dict...")
        scale_code_dict = dict()
        for aid in all_aids.filter(perimeter__isnull=False):
            if aid.perimeter.id not in perimeters_dict:
                self.stdout.write(
                    self.style.ERROR(f'Unknown perimeter: {aid.perimeter}'))
            else:
                aid_codes = perimeters_dict[aid.perimeter.id]['perimeter_contained_codes']
                is_local_aid = aid.perimeter in LOCAL_PERIMETERS
                for code in aid_codes:
                    # init scale_code_dict
                    if code not in scale_code_dict:
                        scale_code_dict[code] = {key: 0 for key in CSV_COLUMNS[1:]}
                    # increment scale_code_dict
                    scale_code_dict[code] = self.increment_scale_code_dict_from_aid(scale_code_dict[code], aid, is_local_aid)
        self.stdout.write(
            self.style.SUCCESS(f"{len(scale_code_dict.keys())} {options['scale']}"))

        self.stdout.write(f'generating data/{SCALE_AIDS_FILE_NAME}.csv file...')
        with open(SCALE_AIDS_FILE_PATH, 'w') as csv_f:
            writer = csv.writer(csv_f)
            writer.writerow(CSV_COLUMNS)
            for code in scale_code_dict:
                writer.writerow([code] + [scale_code_dict[code][key] for key in CSV_COLUMNS[1:]])

    def increment_scale_code_dict_from_aid(self, scale_code_dict, aid, is_local_aid):
        """
        Increment the scale_code_dict keys depending on the aid's characteristics
        """
        # nb_live_aids
        scale_code_dict['nb_live_aids'] += 1
        if is_local_aid:
            scale_code_dict['nb_live_aids_local'] += 1

        # nb_live_aids_type_technical
        if Aid.TYPES.technical in aid.aid_types:
            scale_code_dict['nb_live_aids_type_technical'] += 1
            if is_local_aid:
                scale_code_dict['nb_live_aids_type_technical_local'] += 1

        # nb_live_aids_type_financial
        if Aid.TYPES.financial in aid.aid_types:
            scale_code_dict['nb_live_aids_type_financial'] += 1
            if is_local_aid:
                scale_code_dict['nb_live_aids_type_financial_local'] += 1

        # nb_live_aids_type_legal
        if Aid.TYPES.legal in aid.aid_types:
            scale_code_dict['nb_live_aids_type_legal'] += 1
            if is_local_aid:
                scale_code_dict['nb_live_aids_type_legal_local'] += 1

        # nb_live_aids_category_transition
        if CATEGORY_TRANSITION in aid.categories.all():
            scale_code_dict['nb_live_aids_category_transition'] += 1
            if is_local_aid:
                scale_code_dict['nb_live_aids_category_transition_local'] += 1

        return scale_code_dict
