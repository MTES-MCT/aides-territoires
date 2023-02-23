from model_utils import Choices

ORGANIZATION_TYPE_CHOICES = Choices(
    ("farmer", "Agriculteur"),
    ("association", "Association"),
    ("special", "Collectivité d’outre-mer à statut particulier"),
    ("commune", "Commune"),
    ("department", "Département"),
    ("private_sector", "Entreprise privée"),
    ("public_cies", "Entreprise publique locale (Sem, Spl, SemOp)"),
    ("epci", "Intercommunalité / Pays"),
    ("public_org", "Établissement public (école, bibliothèque…) / Service de l’État"),
    ("private_person", "Particulier"),
    ("region", "Région"),
    ("researcher", "Recherche"),
)

ORGANIZATION_TYPE_CHOICES_WITH_DEFAULT = (
    ("", "Sélectionnez une valeur"),
) + ORGANIZATION_TYPE_CHOICES


ORGANIZATION_TYPES_COLLECTIVITIES_SINGULAR = [
    ("commune", "Commune"),
    ("epci", "Intercommunalité / Pays"),
    ("department", "Département"),
    ("region", "Région"),
    ("special", "Collectivité d’outre-mer à statut particulier"),
]

ORGANIZATION_TYPES_OTHER_SINGULAR = [
    ("public_org", "Établissement public"),
    ("public_cies", "Entreprise publique locale (Sem, Spl, SemOp)"),
    ("association", "Association"),
    ("private_sector", "Entreprise privée"),
    ("private_person", "Particulier"),
    ("farmer", "Agriculteur"),
    ("researcher", "Recherche"),
]

ORGANIZATION_TYPE_CHOICES_COMMUNES_OR_EPCI = Choices(
    ("commune", "Commune"),
    ("epci", "Intercommunalité / Pays"),
)

ORGANIZATION_TYPES_SINGULAR_GROUPED = [
    ("Une collectivité", ORGANIZATION_TYPES_COLLECTIVITIES_SINGULAR),
    ("Un autre bénéficiaire", ORGANIZATION_TYPES_OTHER_SINGULAR),
]
ORGANIZATION_TYPES_SINGULAR_GROUPED_CHOICES = Choices(
    *ORGANIZATION_TYPES_SINGULAR_GROUPED
)

ORGANIZATION_TYPES_SINGULAR_ALL = (
    ORGANIZATION_TYPES_COLLECTIVITIES_SINGULAR + ORGANIZATION_TYPES_OTHER_SINGULAR
)
ORGANIZATION_TYPES_SINGULAR_ALL_CHOICES = Choices(*ORGANIZATION_TYPES_SINGULAR_ALL)

INTERCOMMUNALITY_TYPES = [
    ("CC", "Communauté de communes (CC)"),
    ("CA", "Communauté d’agglomération (CA)"),
    ("CU", "Communauté urbaine (CU)"),
    ("METRO", "Métropole"),
    ("GAL", "Groupe d’action locale (GAL)"),
    ("PNR", "Parc naturel régional (PNR)"),
    ("PETR", "Pays et pôles d’équilibre territorial et rural (PETR)"),
    ("SM", "Syndicat mixte et syndicat de commune"),
]
