from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


# We keep a list of all parameters here,
# to make it easier to included them in the doc
backers_api_parameters = []

q_param = OpenApiParameter(
    name="q",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Rechercher par nom."
    "<br /><br />"
    "Note : il est possible d'avoir des résultats pertinents avec seulement le début du nom.",
    examples=[
        OpenApiExample("", value=""),
        OpenApiExample("ademe", value="ademe"),
        OpenApiExample("conseil régional", value="conseil régional"),
        OpenApiExample("agenc", value="agenc"),
    ],
)
backers_api_parameters.append(q_param)

has_financed_aids_param = OpenApiParameter(
    name="has_financed_aids",
    type=OpenApiTypes.BOOL,
    location=OpenApiParameter.QUERY,
    description="Renvoyer seulement les porteurs d'aides avec des aides.",
    examples=[OpenApiExample("", value=""), OpenApiExample("true", value=True)],
)
backers_api_parameters.append(has_financed_aids_param)

has_published_financed_aids_param = OpenApiParameter(
    name="has_published_financed_aids",
    type=OpenApiTypes.BOOL,
    location=OpenApiParameter.QUERY,
    description="Renvoyer seulement les porteurs d'aides avec des aides publiées.",
    examples=[OpenApiExample("", value=""), OpenApiExample("true", value=True)],
)
backers_api_parameters.append(has_published_financed_aids_param)
