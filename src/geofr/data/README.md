# Geo data

## Fichiers geojson

Les fichier `<scale>-1000m.geojson` proviennent d'Etalab [ici](http://etalab-datasets.geo.data.gouv.fr/contours-administratifs/latest/geojson/)

D'autres sources de données geo :
- https://github.com/gregoiredavid/france-geojson/
- https://www.data.gouv.fr/fr/datasets/decoupage-administratif-communal-francais-issu-d-openstreetmap/ (geojson simplifié)

## Fichiers csv (générés)

Fichiers csv générés grâce à la commande `python manage.py generate_geofr_aids_count`

## Générer une cartographie

```python
import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px

SCALE = 'commune'
DATE = '20210307'
COLUMN_TO_DISPLAY = 'nb_live_aids'  # nb_live_aids_type_technical, nb_live_aids_category_transition

# scale = communes
scale_geojson = gpd.read_file(os.getcwd() + f'/geofr/data/{SCALE}s-1000m.json')
scale_aids_csv = pd.read_csv(os.getcwd() + f'/geofr/data/{SCALE}s_aids_count_{DATE}.csv', dtype={'code': 'str'})
list(scale_aids_csv.columns)

# With matplotlib (image)
merged = pd.merge(scale_geojson, scale_aids_csv, how='inner', left_on='code', right_on='code')
merged.plot(column=COLUMN_TO_DISPLAY, legend=True)
plt.show()

# With plotly (web page, slow...)
fig = px.choropleth(scale_aids_csv, geojson=scale_geojson, featureidkey='properties.code', locations='code', color=COLUMN_TO_DISPLAY)
fig.show()
```
