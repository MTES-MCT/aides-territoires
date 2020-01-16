This module contains scripts used to populate the database of `Perimeter`
objects.

We use Etalab's `decoupage-administratif` package which contains the raw
json data used by the geo api:

https://www.npmjs.com/package/@etalab/decoupage-administratif

Before running those scripts, make sure to run `npm install --dev`.

The scripts in this directory MUST be idempotent, so running them several times
does not produce any side effect.

The scripts MUST be able to create new Perimeters or update existing ones.

The scripts MUST fill the `contained_in` fields for new perimeters.

The scripts MUST NOT delete existing perimeters even if they are not listed
in the data files.

Also, most of those scripts are written in a very inefficient way, because
they are supposed to be ran at most once or twice a year. Indeed, the
raw data is unlikely to change very regularly.

The scripts must be ran in order, since sometimes a script will need data
provided by an other script.

 * populate_countries.py
 * populate_regions.py
 * populate_departments.py
 * populate_overseas.py
 * populate_communes.py
 * populate_epcis.py
 * populate_drainage_basins.py
