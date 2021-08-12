from drf_yasg import openapi


# We keep a list of all parameters here,
# to make it easier to included them in the doc
perimeters_api_parameters = []

q_param = openapi.Parameter(
    'q',
    openapi.IN_QUERY,
    description="""
    Rechercher par nom.

    Exemples : 'lyon', 'par', 'grenble'

    Note : il est possible d'avoir des résultats pertinents avec seulement le début du nom, \
    ou un nom légerement erroné.

    """,
    type=openapi.TYPE_STRING)
perimeters_api_parameters.append(q_param)

scale_param = openapi.Parameter(
    'scale',
    openapi.IN_QUERY,
    description="""
    Filtrer par l'échelle.

    Voir `/perimeters/scales/` pour la liste complète.

    Exemple : 'department'

    """,
    type=openapi.TYPE_STRING)
perimeters_api_parameters.append(scale_param)

# is_visible_to_users_param = openapi.Parameter(
#     'is_visible_to_users',
#     openapi.IN_QUERY,
#     description="""
#     Renvoyer les périmètres cachés.

#     Exemple : 'true'

#     """,
#     type=openapi.TYPE_BOOLEAN)
