from drf_yasg import openapi


# We keep a list of all parameters here,
# to make it easier to included them in the doc
aids_api_parameters = []

text = openapi.Parameter(
    'text',
    openapi.IN_QUERY,
    description="""
    Recherche textuelle.

    Exemples :
    - Chercher "velo" : text=velo
    - Chercher "piste" ou "velo" : text=piste+velo
    - Chercher "piste" et "velo" : text=piste%2Bvelo

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(text)

targeted_audiences = openapi.Parameter(
    'targeted_audiences',
    openapi.IN_QUERY,
    description="""
    La structure pour laquelle vous recherchez des aides.

    Voir `/aids/audiences/` pour la liste complète.

    Exemple :
    - : targeted_audiences=commune
    - : targeted_audiences=department

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(targeted_audiences)

apply_before = openapi.Parameter(
    'apply_before',
    openapi.IN_QUERY,
    description="""
    Candidater avant…

    Exemple : apply_before=2021-09-01

    """,
    type=openapi.FORMAT_DATE)
aids_api_parameters.append(apply_before)

published_after = openapi.Parameter(
    'published_after',
    openapi.IN_QUERY,
    description="""
    Publiée après…

    Exemple : published_after=2020-11-01

    """,
    type=openapi.FORMAT_DATE)
aids_api_parameters.append(published_after)

aid_type = openapi.Parameter(
    'aid_type',
    openapi.IN_QUERY,
    description="""
    Nature de l'aide.

    Voir `/aids/types/` pour la liste complète.

    Exemples :
    - Pour les aides financières : aid_type=financial
    - Pour les aides en ingénieurie aid_type=technical

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(aid_type)

technical_aids = openapi.Parameter(
    'technical_aids',
    openapi.IN_QUERY,
    description="""
    Type d'aides en ingénierie.

    Exemples :
    - Pour les aides en ingénierie de type techniques : technical_aids=technical
    - Pour les aides en ingénierie de type financières : technical_aids=financial
    - Pour les aides en ingénierie de type juridiques et administratives : technical_aids=legal

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(technical_aids)

mobilization_step = openapi.Parameter(
    'mobilization_step',
    openapi.IN_QUERY,
    description="""
    Avancement du projet.

    Voir `/aids/steps/` pour la liste complète.

    Exemples :
    - Pour les aides aux projets en phase "réflexion / conception" : mobilization_step=preop
    - Pour les aides aux projets en phase "Mise en œuvre / réalisation" : mobilization_step=op
    - Pour les aides aux projets en phase "Usage / valorisation" : technical_aids=postop

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(mobilization_step)

destinations = openapi.Parameter(
    'destinations',
    openapi.IN_QUERY,
    description="""
    Actions concernées.

    Voir `/aids/destinations/` pour la liste complète.

    Exemples :
    - Pour les aides qui visent les dépenses de fonctionnement: destinations=supply
    - Pour les aides qui visent les dépenses d'investissement : destinations=investment

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(destinations)

recurrence = openapi.Parameter(
    'recurrence',
    openapi.IN_QUERY,
    description="""
    Récurrence.

    Voir `/aids/recurrences/` pour la liste complète.

    Exemples :
    - Ponctuelle : recurrence=oneoff
    - Permanente : recurrence=ongoing
    - Récurrente : recurrence=recurring

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(recurrence)

call_for_projects_only = openapi.Parameter(
    'call_for_projects_only',
    openapi.IN_QUERY,
    description="""
    Appels à projets / Appels à manifestation d'intérêt uniquement.

    Exemple : call_for_projects_only=true

    """,
    type=openapi.TYPE_BOOLEAN)
aids_api_parameters.append(call_for_projects_only)

perimeter = openapi.Parameter(
    'perimeter',
    openapi.IN_QUERY,
    description="""
    Le territoire.

    Voir `/perimeters/` pour la liste complète.

    Exemple : perimeter=70973-auvergne-rhone-alpes

    Note : passer seulement l'id du périmètre suffit (perimeter=70973).

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(perimeter)

backers = openapi.Parameter(
    'backers',
    openapi.IN_QUERY,
    description="""
    Porteurs d'aides.

    Voir `/backers/` pour la liste complète.

    Exemples :
    - 1 seul porteur : backers=22-ademe
    - plusieurs porteurs (recherche OU) : backers=22-ademe&backers=58-cerema

    Note : passer seulement l'id du (ou des) porteur(s) d'aides suffit (backers=22).

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(backers)

programs = openapi.Parameter(
    'programs',
    openapi.IN_QUERY,
    description="""
    Programmes d'aides.

    Voir `/programs/` pour la liste complète.

    Exemple :
    - 1 seul programme : programs=petites-villes-de-demain
    - plusieurs programmes (recherche OU) :
    programs=petites-villes-de-demain&programs=france-relance

    Note : il faut passer le slug du programme.

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(programs)

themes = openapi.Parameter(
    'themes',
    openapi.IN_QUERY,
    description="""
    Thématiques.

    Voir `/themes/` pour la liste complète.

    Exemples :
    - 1 seule thématique : themes=eau
    - plusieurs thématiques : themes=eau&themes=nature-environnement-risques

    Note : il faut passer le slug de la thématique.

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(themes)

categories = openapi.Parameter(
    'categories',
    openapi.IN_QUERY,
    description="""
    Sous-thématiques.

    Voir `/themes/` pour la liste complète.

    Exemples :
    - 1 seule sous-thématique : categories=eau-potable
    - plusieurs sous-thématiques : categories=eau-potable&categories=eau-de-pluie

    Note : il faut passer le slug de la sous-thématique.

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(categories)

origin_url = openapi.Parameter(
    'origin_url',
    openapi.IN_QUERY,
    description="""
    URL d'origine.

    Exemple : origin_url=http://www.cress-aura.org/actus/mon-ess-lecole-quest-ce-que-cest

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(origin_url)

in_france_relance = openapi.Parameter(
    'in_france_relance',
    openapi.IN_QUERY,
    description="""
    Aides France Relance concernant le MTFP.
    Pour les aides du Plan de relance, utiliser le paramètre `programms`.

    Exemple : in_france_relance=true

    """,
    type=openapi.TYPE_BOOLEAN)
aids_api_parameters.append(in_france_relance)

prevent_generic_filter = openapi.Parameter(
    'prevent_generic_filter',
    openapi.IN_QUERY,
    description="""
    Ce paramètre permet d'empêcher le filtrage par défaut des aides génériques et locales.
    Quand ce paramètre est présent, le résultat de l'API va lister toutes les
    variantes génériques et locales d'une aide - il faut donc s'attendre à ce
    qu'il y ait des aides en doublons.

    Exemple : prevent_generic_filter=yes

    Note : la valeur du paramètre, ici 'yes', n'a pas d'importance,
    puisque la simple présence de ce paramètre suffit.

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(prevent_generic_filter)

order_by = openapi.Parameter(
    'order_by',
    openapi.IN_QUERY,
    description="""
    Trier par.

    Valeurs possibles : relevance (par défaut), publication_date, submission_deadline

    Note : relevance correspond aux aides avec le plus petit périmètre,
    puis aux aides qui expirent bientôt.

    """,
    type=openapi.TYPE_STRING)
aids_api_parameters.append(order_by)
