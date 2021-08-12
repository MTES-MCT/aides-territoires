from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


# We keep a list of all parameters here,
# to make it easier to included them in the doc
perimeters_api_parameters = []

q_param = OpenApiParameter(
    name='q',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Rechercher par nom."
    "<br /><br />"
    "Note : il est possible d'avoir des résultats pertinents avec seulement le début du nom, \
    ou un nom légerement erroné.",
    examples=[
        OpenApiExample('lyon', value='lyon'),
        OpenApiExample('par', value='par'),
        OpenApiExample('grenble', value='grenble')
    ])
perimeters_api_parameters.append(q_param)

scale_param = OpenApiParameter(
    name='scale',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Filtrer par l'échelle."
    "<br /><br />"
    "Voir `/api/perimeters/scales/` pour la liste complète.",
    # enum=[id for (weight, id, name) in Perimeter.SCALES_TUPLE],
    examples=[
        OpenApiExample('Départment', value='department'),
        OpenApiExample('Région', value='region'),
    ])
perimeters_api_parameters.append(scale_param)

# is_visible_to_users_param = OpenApiParameter(
#     name='is_visible_to_users',
#     type=OpenApiTypes.BOOL,
#     location=OpenApiParameter.QUERY,
#     description="""
#     Renvoyer les périmètres cachés.

#     Exemple : 'true'

#     """)
