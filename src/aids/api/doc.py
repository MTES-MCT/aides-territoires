from drf_yasg import openapi


prevent_generic_filter_param = openapi.Parameter(
    'prevent_generic_filter',
    openapi.IN_QUERY,
    description="""
    Ce paramètre permet d'empêcher le filtrage des aides génériques et locales.
    Quand ce paramètre est présent, le résultat de l'API va lister toutes les
    variantes génériques et locales d'une aide - il faut donc s'attendre à ce
    qu'il y ait des aides en doublons.

    Exemple : '?prevent_generic_filter=yes'
    À noter que la valeur du paramètre, ici 'yes', n'a pas d'importance,
    puisque la simple présence de ce paramètre suffit.
    """,
    type=openapi.TYPE_STRING)
