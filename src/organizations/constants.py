from model_utils import Choices

ORGANIZATION_TYPE_CHOICES = Choices(
    ("farmer", "Agriculteur"),
    ("association", "Association"),
    ("special", "Collectivité d'outre-mer à statut particulier"),
    ("commune", "Commune"),
    ("department", "Département"),
    ("private_sector", "Entreprise privée"),
    ("public_cies", "Entreprise publique locale (Sem, Spl, SemOp)"),
    ("epci", "Intercommunalité / Pays"),
    ("public_org", "Établissement public (école, bibliothèque…) / Service de l'État"),
    ("private_person", "Particulier"),
    ("region", "Région"),
    ("researcher", "Recherche"),
)

ORGANIZATION_TYPE_CHOICES_WITH_DEFAULT = (
    ("", "Sélectionnez une valeur"),
) + ORGANIZATION_TYPE_CHOICES
