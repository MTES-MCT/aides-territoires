# Schema du modèle Aid

## Schema ?

Les schémas de données permettent de décrire des modèles de données : quels sont les différents champs, comment sont représentées les données, quelles sont les valeurs possibles etc.

Le schéma respecte le format Table Schema.

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

### Je veux valider un tableur contenant des aides (cas d'un import d'aides)

1. Aller sur le site https://validata.etalab.studio/
2. Dans "Schéma à la carte", insérer l'url du schéma (version française pour ce cas d'usage) : https://raw.githubusercontent.com/MTES-MCT/aides-territoires/aids-schema/src/aids/schema/schema_fr.json
3. Sélectionner un fichier csv/xlsx en local à valider
4. Voir les warnings et les erreurs
    - si c'est pour faire un import dans l'admin, alors l'absence de certains champs dans le fichier ne devrait pas poser problèmes
    - se pencher surtout sur les erreurs "Retirez la colonne XXX non définie dans le schéma" ou "Format incorrect" qui indiquent des erreurs de frappes potentielles

### Je veux valider le schema

```
pip install frictionless

frictionless validate aids/schema/schema.json --type schema
frictionless validate aids/schema/schema_fr.json --type schema
```

### Je veux valider un fichier

```
pip install frictionless

> python
import json, csv
from pprint import pprint
from frictionless import validate, Detector

report = validate('aids/schema/exemple-valide.csv', schema='aids/schema/schema_fr.json', detector=Detector(schema_sync=True))

pprint(report)
```

## Limites actuelles

Les `ChoiceArrayField` qui contiennent des virgules renvoient une erreur. La solution serait d'améliorer leur `pattern` pour éviter de prendre en compte leur virgule... Une autre solution serait d'avoir des csv avec séparateur `;` ?

Les valeurs des champs `ForeignKey` et `ManyToManyField` mappent ensuite à des listes de valeurs contenues dans d'autres tables. Le schéma n'est pas capable d'aller récupérer et stocker ces infos, donc aucune vérification n'est faite sur ces colonnes.

Il faut mettre à jour le schéma manuellement, donc ne pas oublier de lancer la commande au grès des mises à jour du modèle `Aid`.
