from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from aids.models import Aid
from aids.forms import AidSearchForm
from aids.constants import (
    AUDIENCES_ALL,
    AID_TYPE_CHOICES, FINANCIAL_AIDS, TECHNICAL_AIDS, OTHER_AIDS)


# We keep a list of all parameters here,
# to make it easier to included them in the doc
aids_api_parameters = []

text = OpenApiParameter(
    name='text',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Recherche textuelle.",
    examples=[
        OpenApiExample('velo', value='velo'),
        OpenApiExample('piste OU velo', value='piste+velo'),
        OpenApiExample('piste ET velo', value='piste%2Bvelo')
    ])
aids_api_parameters.append(text)

targeted_audiences = OpenApiParameter(
    name='targeted_audiences',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="La structure pour laquelle vous recherchez des aides."
    "<br /><br />"
    "Voir aussi `/api/aids/audiences/` pour la liste complète.",
    enum=[id for (id, key) in AUDIENCES_ALL],
    examples=[
        OpenApiExample('Commune', value='commune'),
        OpenApiExample('Départment', value='department')
    ])
aids_api_parameters.append(targeted_audiences)

apply_before = OpenApiParameter(
    name='apply_before',
    type=OpenApiTypes.DATE,
    location=OpenApiParameter.QUERY,
    description="Candidater avant…",
    examples=[
        OpenApiExample('2021-09-01', value='2021-09-01')
    ])
aids_api_parameters.append(apply_before)

published_after = OpenApiParameter(
    name='published_after',
    type=OpenApiTypes.DATE,
    location=OpenApiParameter.QUERY,
    description="Publiée après…",
    examples=[
        OpenApiExample('2020-11-01', value='2020-11-01')
    ])
aids_api_parameters.append(published_after)

aid_type = OpenApiParameter(
    name='aid_type',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Nature de l'aide.",
    enum=[id for (id, name) in AID_TYPE_CHOICES],
    examples=[
        OpenApiExample('Aides financières', value='financial'),
        OpenApiExample('Aides en ingénierie', value='technical')
    ])
aids_api_parameters.append(aid_type)

financial_aids = OpenApiParameter(
    name='financial_aids',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Type d'aides financières."
    "<br /><br />"
    "Voir aussi `/api/aids/types/` pour la liste complète.",
    enum=[id for (id, name) in FINANCIAL_AIDS + OTHER_AIDS],
    examples=[OpenApiExample(name, value=id) for (id, name) in FINANCIAL_AIDS + OTHER_AIDS])
aids_api_parameters.append(financial_aids)

technical_aids = OpenApiParameter(
    name='technical_aids',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Type d'aides en ingénierie."
    "<br /><br />"
    "Voir aussi `/api/aids/types/` pour la liste complète.",
    enum=[id for (id, name) in TECHNICAL_AIDS],
    examples=[OpenApiExample(name, value=id) for (id, name) in TECHNICAL_AIDS])
aids_api_parameters.append(technical_aids)

mobilization_step = OpenApiParameter(
    name='mobilization_step',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Avancement du projet."
    "<br /><br />"
    "Voir aussi `/api/aids/steps/` pour la liste complète.",
    enum=[id for (id, name) in Aid.STEPS],
    examples=[OpenApiExample(name, value=id) for (id, name) in Aid.STEPS])
aids_api_parameters.append(mobilization_step)

destinations = OpenApiParameter(
    name='destinations',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Actions concernées."
    "<br /><br />"
    "Voir aussi `/api/aids/destinations/` pour la liste complète.",
    enum=[id for (id, name) in Aid.DESTINATIONS],
    examples=[OpenApiExample(name, value=id) for (id, name) in Aid.DESTINATIONS])
aids_api_parameters.append(destinations)

recurrence = OpenApiParameter(
    name='recurrence',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Récurrence."
    "<br /><br />"
    "Voir aussi `/api/aids/recurrences/` pour la liste complète.",
    enum=[id for (id, name) in Aid.RECURRENCES],
    examples=[OpenApiExample(name, value=id) for (id, name) in Aid.RECURRENCES])
aids_api_parameters.append(recurrence)

call_for_projects_only = OpenApiParameter(
    name='call_for_projects_only',
    type=OpenApiTypes.BOOL,
    location=OpenApiParameter.QUERY,
    description="Appels à projets / Appels à manifestation d'intérêt uniquement.",
    examples=[
        OpenApiExample('true', value=True),
    ])
aids_api_parameters.append(call_for_projects_only)

perimeter = OpenApiParameter(
    name='perimeter',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Le territoire."
    "<br /><br />"
    "Voir `/api/perimeters/` pour la liste complète."
    "<br /><br />"
    "Note : passer seulement l'id du périmètre suffit (perimeter=70973).",
    examples=[
        OpenApiExample('70973-auvergne-rhone-alpes', value='70973-auvergne-rhone-alpes'),
        OpenApiExample('95861-clermont-ferrand', value='95861-clermont-ferrand'),
        OpenApiExample('109957-pays-cevennes', value='109957-pays-cevennes')
    ])
aids_api_parameters.append(perimeter)

backers = OpenApiParameter(
    name='backers',
    type={'type': 'array', 'items': {'type': 'string'}},
    location=OpenApiParameter.QUERY,
    description="Porteurs d'aides."
    "<br /><br />"
    "Voir `/api/backers/` pour la liste complète."
    "<br /><br />"
    "Notes : "
    "<br />"
    "- possible de passer plusieurs porteurs (recherche OU)"
    "<br />"
    "- passer seulement l'id du (ou des) porteur(s) d'aides suffit (backers=22)",
    examples=[
        OpenApiExample('22-ademe', value='22-ademe'),
        OpenApiExample('113-banque-des-territoires', value='113-banque-des-territoires')
    ])
aids_api_parameters.append(backers)

programs = OpenApiParameter(
    name='programs',
    type={'type': 'array', 'items': {'type': 'string'}},
    location=OpenApiParameter.QUERY,
    description="Programmes d'aides."
    "<br /><br />"
    "Voir `/api/programs/` pour la liste complète."
    "<br /><br />"
    "Notes : "
    "<br />"
    "- possible de passer plusieurs programmes (recherche OU)"
    "<br />"
    "- il faut passer le slug du (ou des) programme(s)",
    examples=[
        OpenApiExample('Petites villes de demain', value='petites-villes-de-demain'),
        OpenApiExample('France Relance', value='france-relance')
    ])
aids_api_parameters.append(programs)

themes = OpenApiParameter(
    name='themes',
    type={'type': 'array', 'items': {'type': 'string'}},
    location=OpenApiParameter.QUERY,
    description="Thématiques."
    "<br /><br />"
    "Voir `/api/themes/` pour la liste complète."
    "<br /><br />"
    "Notes : "
    "<br />"
    "- possible de passer plusieurs thématiques (recherche OU)"
    "<br />"
    "- il faut passer le slug de la (ou des) thématique(s)",
    examples=[
        OpenApiExample('Énergies / Déchets', value='energies-dechets'),
        OpenApiExample('Nature / environnement', value='nature-environnement-risques')
    ])
aids_api_parameters.append(themes)

categories = OpenApiParameter(
    name='categories',
    type={'type': 'array', 'items': {'type': 'string'}},
    location=OpenApiParameter.QUERY,
    description="Sous-thématiques."
    "<br /><br />"
    "Voir `/api/themes/` pour la liste complète."
    "<br /><br />"
    "Notes : "
    "<br />"
    "- possible de passer plusieurs sous-thématiques (recherche OU)"
    "<br />"
    "- il faut passer le slug de la (ou des) sous-thématique(s)",
    examples=[
        OpenApiExample('Attractivité économique', value='attractivite'),
        OpenApiExample('Transition énergétique', value='transition-energetique')
    ])
aids_api_parameters.append(categories)

origin_url = OpenApiParameter(
    name='origin_url',
    type=OpenApiTypes.URI,
    location=OpenApiParameter.QUERY,
    description="URL d'origine.",
    examples=[
        OpenApiExample('URL', value='http://www.cress-aura.org/actus/mon-ess-lecole-quest-ce-que-cest'),  # noqa
    ])
aids_api_parameters.append(origin_url)

in_france_relance = OpenApiParameter(
    name='in_france_relance',
    type=OpenApiTypes.BOOL,
    location=OpenApiParameter.QUERY,
    description="Aides France Relance concernant le MTFP."
    "<br /><br />"
    "Pour les aides du Plan de relance, utiliser le paramètre `programs`.",
    examples=[
        OpenApiExample('true', value=True),
    ])
aids_api_parameters.append(in_france_relance)

prevent_generic_filter = OpenApiParameter(
    name='prevent_generic_filter',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Ce paramètre permet d'empêcher le filtrage par défaut \
    des aides génériques et locales. Quand ce paramètre est présent, \
    le résultat de l'API va lister toutes les variantes génériques et locales d'une aide. \
    Il faut donc s'attendre à ce qu'il y ait des aides en doublon."
    "<br /><br />"
    "Note : la valeur du paramètre, ici 'yes', n'a pas d'importance, \
    puisque la simple présence de ce paramètre suffit.",
    examples=[
        OpenApiExample('true', value=True),
    ])
aids_api_parameters.append(prevent_generic_filter)

order_by = OpenApiParameter(
    name='order_by',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Trier par."
    "<br /><br />"
    "Note : relevance correspond aux aides avec le plus petit périmètre, \
    puis aux aides qui expirent bientôt.",
    enum=[id for (id, name) in AidSearchForm.ORDER_BY],
    examples=[OpenApiExample(name, value=id) for (id, name) in AidSearchForm.ORDER_BY])
aids_api_parameters.append(order_by)
