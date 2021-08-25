# Table Schema du modèle Aid


## Table Schema ?

Frictionless
https://specs.frictionlessdata.io/table-schema/
https://github.com/frictionlessdata/datapackage-py

Etalab
https://schema.data.gouv.fr/
https://publier.etalab.studio/

## Comment le générer/mettre à jour ?

Le script se trouve ici : `/src/aids/management/commmands/generate_aids_table_schema.py`

Comment le lancer :
```
python manage.py generate_aids_table_schema
```

Il va générer 2 fichiers json :
- `schema.json` où les noms des champs et les choix seront en anglais
- `schema_fr.json` où les noms des champs et les choix seront traduits en français

## Usage

