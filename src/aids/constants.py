# Aid Audiences

COLLECTIVITIES_AUDIENCES = (
    ("commune", "Communes"),
    ("epci", "Intercommunalités / Pays"),
    ("department", "Départements"),
    ("region", "Régions"),
    ("special", "Collectivités d'outre-mer à statuts particuliers"),
)

OTHER_AUDIENCES = (
    ("association", "Associations"),
    ("private_person", "Particuliers"),
    ("farmer", "Agriculteurs"),
    ("private_sector", "Entreprises privées"),
    ("public_cies", "Entreprises publiques locales (Sem, Spl, SemOp)"),
    (
        "public_org",
        "Établissements publics (écoles, bibliothèques…) / Services de l'État",
    ),
    ("researcher", "Recherche"),
)

AUDIENCES_ALL = COLLECTIVITIES_AUDIENCES + OTHER_AUDIENCES

AUDIENCES_GROUPED = (
    ("Collectivités", COLLECTIVITIES_AUDIENCES),
    ("Autres bénéficiaires", OTHER_AUDIENCES),
)


# Aid Types

FINANCIAL_AIDS = (
    ("grant", "Subvention"),
    ("loan", "Prêt"),
    ("recoverable_advance", "Avance récupérable"),
    ("cee", "Certificat d'économie d'énergie (CEE)"),
)

OTHER_AIDS = (("other", "Autre aide financière"),)

ALL_FINANCIAL_AIDS = FINANCIAL_AIDS + OTHER_AIDS

FINANCIAL_AIDS_LIST = ("grant", "loan", "recoverable_advance", "other", "cee")

TECHNICAL_AIDS = (
    ("technical_engineering", "Ingénierie technique"),
    ("financial_engineering", "Ingénierie financière"),
    ("legal_engineering", "Ingénierie Juridique / administrative"),
)

TECHNICAL_AIDS_LIST = (
    "technical_engineering",
    "financial_engineering",
    "legal_engineering",
)

AID_TYPES_ALL = FINANCIAL_AIDS + TECHNICAL_AIDS + OTHER_AIDS

AID_TYPES_GROUPED = (
    ("Aides financières", FINANCIAL_AIDS + OTHER_AIDS),
    ("Aides en ingénierie", TECHNICAL_AIDS),
)

AID_TYPES_GROUPS = (
    ("financial_group", "Aide financière"),
    ("technical_group", "Aide en ingénierie"),
)

AID_TYPES_ALL_WITH_GROUPS = AID_TYPES_ALL + AID_TYPES_GROUPS
