# flake8: noqa

v14_changes = "" \
    "**Aides** : ajout du champ `is_call_for_project`<br />" \
    "Ajout de nouveaux points d'entrée : **Programmes**, **Thématiques** et **Périmètres**<br />" \
    "Documentation de l'API au format OpenAPI 3"

v13_changes = "" \
    "**Aides** : ajout des champs `loan_amount` and `recoverable_advance_amount`<br />" \
    "**Aides** : suppression du champ `tags`"

description = f"""

#### Documentation

|Version       |Description des changements|
|--------------|---------------------------|
|1.4 (actuelle)|{v14_changes}|
|1.3           |{v13_changes}|
|1.2           |**Aides** : ajout du champ `categories`|
|1.1           |**Aides** : ajout du champ `programs`|
|1.0           |Première version de l'API 🎉<br /> Points d'entrée : **Aides** et **Porteurs d'aides**|

"""
