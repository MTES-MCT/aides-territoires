This module contains almost only legacy code.

The scripts in this directory were used once to populate the `Perimeter`
database with french's regions, departments, communes, epcis, etc.

Since some of that data is unlikely to change regularly (e.g regions,
departments), most of those task MUST not be ran again.

However, some other tasks were modified to handle updates of existing data:

 - populate_communes.py
 - populate_epcis.py
 - populate_drainage_basins.py
