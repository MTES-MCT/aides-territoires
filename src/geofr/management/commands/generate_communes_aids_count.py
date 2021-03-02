import os
import csv

from django.core.management.base import BaseCommand

from aids.models import Aid
from geofr.utils import perimeters_to_dict_with_contained


AIDS_PER_COMMUNE_CSV = os.path.dirname(os.path.realpath(__file__)) + '/../../data/communes_aids_count.csv'  # noqa


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_aids = Aid.objects \
            .select_related('perimeter') \
            .live()

        print('generating perimeters_dict...')
        perimeters_dict = perimeters_to_dict_with_contained()

        print('generating communes_dict...')
        communes_dict = dict()
        for aid in all_aids:
            if aid.perimeter:
                if aid.perimeter.id not in perimeters_dict:
                    print('Unknown perimeter', aid.perimeter)
                else:
                    aid_communes_insee = perimeters_dict[aid.perimeter.id]['perimeter_contained_insee']  # noqa
                    for insee in aid_communes_insee:
                        if insee in communes_dict:
                            communes_dict[insee] += 1
                        else:
                            communes_dict[insee] = 1

        print('generating data/commmunes_aids_count.csv file...')
        with open(AIDS_PER_COMMUNE_CSV, 'w') as csv_f:
            writer = csv.writer(csv_f)
            writer.writerow(['communeINSEE', 'aidsCount'])
            for insee in communes_dict:
                writer.writerow([insee, communes_dict[insee]])


"""
# Generate graph

import os
import plotly.express as px
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

communes_geojson = gpd.read_file(os.getcwd() + '/communes-20190101.json')
communes_aids_csv = pd.read_csv(os.getcwd() + '/geofr/data/commune_aids_count.csv')  # noqa

merged = pd.merge(communes_geojson, communes_aids_csv, how='inner', left_on='insee', right_on='communeINSEE')  # noqa

merged.plot(column='aidsCount')
plt.show()
"""
