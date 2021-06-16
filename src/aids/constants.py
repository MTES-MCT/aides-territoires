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

AUDIENCES_GROUPED = (
    ('Collectivités', COLLECTIVITIES_AUDIENCES),
    ('Autres bénéficiaires', OTHER_AUDIENCES)
)
