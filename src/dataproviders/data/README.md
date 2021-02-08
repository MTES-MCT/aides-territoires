This folder contains configuration files that are used during 
imports of external data sources.

External data sources often have different classifications from ours
concerning Perimeters, Target Audiences, Themes & Categories, etc

Therefore we need to map their terminologies to our DB values.

We used to do it directly in the import commands.
But having a CSV flat file helps in terms of readability and updating it if needed.

Sometimes an external terminology will map to multiple instances of our DB.
For instance : `Agriculture` --> `Agriculture et agroalimentaire`& `Consommation et production`
Therefore we sometimes need multiple columns on AT side.

**Nouvelle Aquitaine RSS**

Two mapping files were created with the help of Jo.
- Target audiences
- Categories

Used in `src/dataproviders/management/commands/import_nouvelle_aquitaine_rss.py`
