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

"""
technical_engineering and legal_engineering are now divided in multiple choices
 but we keep them in TECHNICAL_AIDS list to handle the merge command
 we will delete them after the merge command.
 To not displayed technical_engineering and legal_engineering choices
 but only new choices in front we use TECHNICAL_AIDS_FOR_FRONT_PURPOSE list
"""
TECHNICAL_AIDS = (
    ("technical_engineering", "Ingénierie technique"),
    ("strategic_engineering", "Ingénierie de planification et stratégie"),
    ("diagnostic_engineering", "Ingénierie d’études et diagnostiques"),
    ("AMOA_engineering", "AMOA / MOD"),
    ("MOE_engineering", "MOE / MOE déléguée"),
    ("financial_engineering", "Ingénierie financière"),
    ("legal_engineering", "Ingénierie Juridique / administrative"),
    ("administrative_engineering", "Ingénierie administrative"),
    ("legal_and_regulatory_engineering", "Ingénierie juridique et réglementaire"),
    ("formation_engineering", "Formation / montée en compétence"),
)

TECHNICAL_AIDS_FOR_FRONT_PURPOSE = (
    ("strategic_engineering", "Ingénierie de planification et stratégie"),
    ("diagnostic_engineering", "Ingénierie d’études et diagnostiques"),
    ("AMOA_engineering", "AMOA / MOD"),
    ("MOE_engineering", "MOE / MOE déléguée"),
    ("financial_engineering", "Ingénierie financière"),
    ("administrative_engineering", "Ingénierie administrative"),
    ("legal_and_regulatory_engineering", "Ingénierie juridique et réglementaire"),
    ("formation_engineering", "Formation / montée en compétence"),
)

TECHNICAL_ENGINEERING_AIDS = (
    ("strategic_engineering", "Ingénierie de planification et stratégie"),
    ("diagnostic_engineering", "Ingénierie d’études et diagnostiques"),
    ("AMOA_engineering", "AMOA / MOD"),
    ("MOE_engineering", "MOE / MOE déléguée"),
)

LEGAL_AND_ADMINISTRATIVE_ENGINEERING_AIDS = (
    ("administrative_engineering", "Ingénierie administrative"),
    ("legal_and_regulatory_engineering", "Ingénierie juridique et réglementaire"),
)

TECHNICAL_AIDS_LIST = (
    "strategic_engineering",
    "diagnostic_engineering",
    "AMOA_engineering",
    "MOE_engineering",
    "financial_engineering",
    "administrative_engineering",
    "legal_and_regulatory_engineering",
    "formation_engineering",
)

AID_TYPES_ALL = FINANCIAL_AIDS + TECHNICAL_AIDS + OTHER_AIDS

AID_TYPES_ALL_FOR_FRONT_PURPOSES = (
    FINANCIAL_AIDS + TECHNICAL_AIDS_FOR_FRONT_PURPOSE + OTHER_AIDS
)

AID_TYPES_GROUPED = (
    ("Aides financières", FINANCIAL_AIDS + OTHER_AIDS),
    ("Aides en ingénierie", TECHNICAL_AIDS_FOR_FRONT_PURPOSE),
)

AID_TYPES_GROUPS = (
    ("financial_group", "Aide financière"),
    ("technical_group", "Aide en ingénierie"),
)

AID_TYPES_ALL_WITH_GROUPS = AID_TYPES_ALL + AID_TYPES_GROUPS
