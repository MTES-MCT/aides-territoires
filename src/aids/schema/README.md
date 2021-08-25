# Table Schema du modèle Aid


## Table Schema ?

Frictionless
- https://specs.frictionlessdata.io/table-schema/
- https://github.com/frictionlessdata/datapackage-py

Etalab
- https://schema.data.gouv.fr/
- https://publier.etalab.studio/
- https://validata.etalab.studio/

## Comment le générer/mettre à jour ?

Le script se trouve ici : `/src/aids/management/commmands/generate_aids_table_schema.py`

Comment le lancer :
```
python manage.py generate_aids_table_schema
```

Il va générer 2 fichiers json :
- `schema.json` où les noms des champs et les choix sont en anglais
- `schema_fr.json` où les noms des champs et les choix sont traduits en français

## Usage

### Je veux valider un csv avec des aides (cas d'un import d'aides)

1. Aller sur le site https://validata.etalab.studio/
2. Dans "Schéma à la carte", insérer l'url du schéma (version française pour ce cas d'usage) : https://raw.githubusercontent.com/MTES-MCT/aides-territoires/aids-schema/src/aids/schema/schema_fr.json
3. Sélectionner un fichier csv/xlsx en local à valider
4. Voir les warnings et les erreurs
    - si c'est pour faire un import dans l'admin, alors l'absence de certains champs dans le fichier ne devrait pas poser problèmes
    - se pencher surtout sur les erreurs "Retirez la colonne XXX non définie dans le schéma" ou "Format incorrect" qui indiquent des erreurs de frappes potentielles
