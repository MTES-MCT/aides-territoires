from model_utils import Choices

ORGANIZATION_TYPE = Choices(
    ('farmer', 'Agriculteur'),
    ('association', 'Association'),
    ('special', "Collectivité d'outre-mer à statut particulier"),
    ('commune', 'Commune'),
    ('department', 'Département'),
    ('private_sector', 'Entreprises privée'),
    ('public_cies', "Entreprise publique locale (Sem, Spl, SemOp)"),
    ('epci', 'EPCI à fiscalité propre'),
    ('public_org', "Établissement public (école, bibliothèque…) / Service de l'État"),
    ('private_person', 'Particulier'),
    ('region', 'Région'),
    ('researcher', 'Recherche'),
)
