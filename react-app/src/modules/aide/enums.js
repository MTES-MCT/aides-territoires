// les périmètres géographiques éligibles pour l'aide
export const PERIMETRE_APPLICATION_OPTIONS = [
  { value: "commune", label: "Commune" },
  { value: "departement", label: "Département" },
  { value: "region", label: "Régionale" },
  { value: "outre_mer", label: "Outre Mer" },
  { value: "metropole", label: "France (hors Outre-mer)" },
  { value: "france", label: "France et Outre-mer" },
  { value: "europe", label: "Europe" }
];

export const PERIMETRE_DIFFUSION_OPTIONS = [
  { value: "europe", label: "Europe" },
  { value: "metropole", label: "National" },
  { value: "outre_mer", label: "Outre Mer" },
  { value: "region", label: "Régional" },
  { value: "departement", label: "Départemental" },
  { value: "autre", label: "Autre" }
];
// ajouter: convention
export const FORME_DE_DIFFUSION_OPTIONS = [
  {
    value: "subvention",
    label: "Subvention"
  },
  {
    value: "pret",
    label: "prêt"
  },
  {
    value: "convention",
    label: "Convention"
  },
  {
    value: "bonification_interet",
    label: "Bonification d'intérêt"
  },
  {
    value: "avance_recuperable",
    label: "avance récupérable"
  },
  {
    value: "garantie",
    label: "Garantie"
  },
  {
    value: "investissement_en_capital",
    label: "Investissement en capital"
  },
  {
    value: "avantage_fiscal",
    label: "avantage fiscal"
  },
  {
    value: "fonds_de_retour",
    label: "Fonds de retour"
  }
];

export const TYPE_OPTIONS = [
  { value: "financement", label: "Financier" },
  { value: "autre", label: "Non-financier" }
];

export const ETAPE_OPTIONS = [
  {
    value: "pre_operationnel",
    label: "Pré-opérationnel (Avant-projet, faisabilité)"
  },
  {
    value: "operationnel",
    label: "Opérationnel (Programmation-conception-réalisation)"
  },
  {
    value: "fonctionnement",
    label: "Fonctionnement (Fonctionnement,Phase de vie)"
  }
];

export const STATUS_PUBLICATION_OPTIONS = [
  {
    value: "draft",
    label: "Brouillon"
  },
  {
    value: "review_required",
    label: "A vérifier"
  },
  {
    value: "published",
    label: "Publiée"
  }
];

export const BENEFICIAIRES_OPTIONS = [
  {
    value: "commune",
    label: "Commune"
  },
  {
    value: "EPCI",
    label: "EPCI"
  },
  {
    value: "societe_civile",
    label: "Société civile"
  },
  {
    value: "entreprises",
    label: "Entreprises"
  },
  {
    value: "associations",
    label: "Associations"
  },
  {
    value: "autre",
    label: "Autre"
  }
];

export const DESTINATION_OPTIONS = [
  {
    value: "investissement",
    label: "Investissement"
  },
  {
    value: "fonctionnement",
    label: "Fonctionnement"
  },
  {
    value: "etude",
    label: "Etude"
  },
  {
    value: "fourniture",
    label: "Fourniture"
  },
  {
    value: "service",
    label: "Service"
  },
  {
    value: "travaux",
    label: "Travaux"
  },
  {
    value: "autre",
    label: "Autre"
  }
];

export const THEMATIQUES_OPTIONS = [
  {
    value: "amenagement_durable",
    label: "Aménagement Durable"
  },
  {
    value: "developpement_local",
    label: "Développement local"
  },
  {
    value: "infrastructures_reseaux_et_deplacements",
    label: "Infrastructures, réseaux et déplacements"
  },
  {
    value: "solidarite_et_cohesion_sociale",
    label: "Solidarité et Cohésion sociale"
  }
];

export const STATUS_OPTIONS = [
  {
    value: "ouvert",
    label: "Ouvert"
  },
  {
    value: "projete",
    label: "Projeté"
  },
  {
    value: "ferme",
    label: "Fermé"
  }
];
