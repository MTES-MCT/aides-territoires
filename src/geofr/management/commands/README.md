This module contains scripts used to populate the database of `Perimeter`
objects ("populate_*.py" scripts)


The following scripts use Etalab's `decoupage-administratif` package, which
contains the raw json data used by the geo api, to create all "Collectivités
locales". They MUST be run in order, since sometimes a script will need data
provided by an other script.

 * python manage.py populate_countries
 * python manage.py populate_regions
 * python manage.py populate_departments
 * python manage.py populate_overseas
 * python manage.py populate_communes
 * python manage.py populate_epcis

Alternatively, the script populate_all_collectivities is equivalent to running
the previous list of scripts in order.
 * python manage.py populate_all_collectivities


Some scripts use data that is more exotic. When that happens, each script
describes where does the data comes from.

These special scripts MUST follow the rules described at the top of 
geofr/services/populate.py.

They MUST be run only after the "collectivités locales" are created.

 * python manage.py populate_drainage_basins
 * python manage.py populate_scots
