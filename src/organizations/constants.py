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

# Source: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033878299/
POPULATION_STRATAS = [
    ("500-", "communes de 0 à 499 habitants"),
    ("500_599", "communes de 500 à 999 habitants"),
    ("1000_1999", "communes de 1 000 à 1 999 habitants"),
    ("2000_3499", "communes de 2 000 à 3 499 habitants"),
    ("3500_4999", "communes de 3 500 à 4 999 habitants"),
    ("5000_7499", "communes de 5 000 à 7 499 habitants"),
    ("7500_9999", "communes de 7 500 à 9 999 habitants"),
    ("10000_14999", "communes de 10 000 à 14 999 habitants"),
    ("15000_19999", "communes de 15 000 à 19 999 habitants"),
    ("20000_34999", "communes de 20 000 à 34 999 habitants"),
    ("35000_49999", "communes de 35 000 à 49 999 habitants"),
    ("50000_74999", "communes de 50 000 à 74 999 habitants"),
    ("75000_99999", "communes de 75 000 à 99 999 habitants"),
    ("100000_199999", "communes de 100 000 à 199 999 habitants"),
    ("200000+", "communes de 200 000 habitants et plus"),
]
