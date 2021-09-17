# Aid Audiences

COLLECTIVITIES_AUDIENCES = (
    ('commune', 'Communes'),
    ('epci', 'EPCI à fiscalité propre'),
    ('department', 'Départements'),
    ('region', 'Régions'),
    ('special', "Collectivités d'outre-mer à statuts particuliers"),
)

OTHER_AUDIENCES = (
    ('association', 'Associations'),
    ('private_person', 'Particuliers'),
    ('farmer', 'Agriculteurs'),
    ('private_sector', 'Entreprises privées'),
    ('public_cies', "Entreprises publiques locales (Sem, Spl, SemOp)"),
    ('public_org', "Établissements publics (écoles, bibliothèques…) / Services de l'État"),
    ('researcher', 'Recherche'),
)

AUDIENCES_ALL = COLLECTIVITIES_AUDIENCES + OTHER_AUDIENCES

AUDIENCES_GROUPED = (
    ('Collectivités', COLLECTIVITIES_AUDIENCES),
    ('Autres bénéficiaires', OTHER_AUDIENCES)
)


# Aid Types

FINANCIAL_AIDS = (
    ('grant', 'Subvention'),
    ('loan', 'Prêt'),
    ('recoverable_advance', 'Avance récupérable'),
)

OTHER_AIDS = (
    ('other', 'Autre aide financière'),
)

FINANCIAL_AIDS_LIST = ('grant', 'loan', 'recoverable_advance', 'other')

TECHNICAL_AIDS = (
    ('technical', 'Ingénierie technique'),
    ('financial', 'Ingénierie financière'),
    ('legal', 'Ingénierie Juridique / administrative'),
)

TECHNICAL_AIDS_LIST = ('technical', 'financial', 'legal')

TYPES_ALL = FINANCIAL_AIDS + TECHNICAL_AIDS + OTHER_AIDS

TYPES_GROUPED = (
    ('Aides financières', FINANCIAL_AIDS + OTHER_AIDS),
    ('Aides en ingénierie', TECHNICAL_AIDS),
)

AID_TYPE_CHOICES = (
    ('financial', 'Aide financière'),
    ('technical', 'Aide en ingénierie'),
)
