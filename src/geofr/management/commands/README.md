This module contains scripts used to populate the database of `Perimeter`
objects.

We use Etalab's `decoupage-administratif` package which contains the raw
json data used by the geo api:

https://github.com/etalab/decoupage-administratif

Some scripts use data that is more exotic. When that happens, each script
describes where does the data comes from.

The scripts in this directory MUST be idempotent, so running them several times
does not produce any side effect.

The scripts MUST be able to create new Perimeters or update existing ones.

The scripts MUST fill the `contained_in` fields for new perimeters.

The scripts MUST NOT delete existing perimeters even if they are not listed
in the data files.

The scripts MUST be ran in order, since sometimes a script will need data
provided by an other script.

Also, most of those scripts are written in a very inefficient way, because
they are supposed to be ran at most once or twice a year. Indeed, the
raw data is unlikely to change very regularly.


 * python manage.py populate_countries
 * python manage.py populate_regions
 * python manage.py populate_departments
 * python manage.py populate_overseas
 * python manage.py populate_communes
 * python manage.py populate_epcis
 * python manage.py populate_drainage_basins
 * python manage.py populate_scots
