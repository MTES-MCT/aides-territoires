from drf_yasg import openapi


# We keep a list of all parameters here,
# to make it easier to included them in the doc
backers_api_parameters = []

q_param = openapi.Parameter(
    'q',
    openapi.IN_QUERY,
    description="""
    Rechercher par nom.

    Exemples : 'ademe', 'conseil régional', 'agenc'

    Note : il est possible d'avoir des résultats pertinents avec seulement le début du nom.

    """,
    type=openapi.TYPE_STRING)
backers_api_parameters.append(q_param)

has_financed_aids_param = openapi.Parameter(
    'has_financed_aids',
    openapi.IN_QUERY,
    description="""
    Renvoyer seulement les porteurs d'aides avec des aides.

    Exemple : 'true'
    """,
    type=openapi.TYPE_BOOLEAN)
backers_api_parameters.append(has_financed_aids_param)

has_published_financed_aids_param = openapi.Parameter(
    'has_published_financed_aids',
    openapi.IN_QUERY,
    description="""
    Renvoyer seulement les porteurs d'aides avec des aides publiées.

    Exemple : 'true'
    """,
    type=openapi.TYPE_BOOLEAN)
backers_api_parameters.append(has_published_financed_aids_param)
