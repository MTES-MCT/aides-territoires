from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from geofr.models import Perimeter


# We keep a list of all parameters here,
# to make it easier to included them in the doc
perimeters_api_parameters = []
perimeterdata_api_parameters = []

q_param = OpenApiParameter(
    name="q",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Rechercher par nom."
    "<br /><br />"
    "Note : il est possible d'avoir des résultats pertinents avec seulement le début du nom, \
    ou un nom légerement erroné.",
    examples=[
        OpenApiExample("", value=""),
        OpenApiExample("lyon", value="lyon"),
        OpenApiExample("par", value="par"),
        OpenApiExample("grenble", value="grenble"),
    ],
)
perimeters_api_parameters.append(q_param)

scale_param = OpenApiParameter(
    name="scale",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Filtrer par l'échelle."
    "<br /><br />"
    "Voir `/api/perimeters/scales/` pour la liste complète.",
    enum=[id for (weight, id, name) in Perimeter.SCALES_TUPLE],
    examples=[OpenApiExample("", value="")]
    + [OpenApiExample(name, value=id) for (weight, id, name) in Perimeter.SCALES_TUPLE],
)
perimeters_api_parameters.append(scale_param)

perimeter_code_param = OpenApiParameter(
    name="perimeter_code",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Show the extra data for the specified perimeter",
    examples=[
        OpenApiExample("Paris", value="75056"),
        OpenApiExample("Dinan", value="22050"),
        OpenApiExample("", value=""),
    ],
)
perimeterdata_api_parameters.append(perimeter_code_param)
