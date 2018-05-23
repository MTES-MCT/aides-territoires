// les périmètres géographiques éligibles pour l'aide
const enums = {
  perimetreApplicationType: [
    { value: "commune", label: "Commune" },
    { value: "departement", label: "Département" },
    { value: "region", label: "Région" },
    { value: "outre_mer", label: "Outre Mer" },
    { value: "metropole", label: "Métropole" },
    { value: "france", label: "Métropole et Outre-mer" },
    { value: "europe", label: "Europe" }
  ],
  perimetreDiffusionType: [
    { value: "europe", label: "Europe" },
    { value: "metropole", label: "National" },
    { value: "outre_mer", label: "Outre Mer" },
    { value: "region", label: "Régional" },
    { value: "departement", label: "Départemental" },
    { value: "autre", label: "Autre" }
  ],
  formeDeDiffusion: [
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
    },
    {
      value: "autre",
      label: "Autre"
    }
  ],
  type: [
    { value: "financement", label: "Financier" },
    { value: "autre", label: "Non-financier" }
  ],
  etape: [
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
  ],
  statusPublication: [
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
  ],
  beneficiaires: [
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
  ],
  destination: [
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
  ],
  thematiques: [
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
  ],
  status: [
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
  ],
  categorieParticuliere: [
    {
      value: "AAP",
      label: "AAP"
    },
    {
      value: "AMI",
      label: "AMI"
    }
  ]
};

export function getLabelFromEnumId(enumId, enumValue) {
  for (let i = 0; i < enums[enumId].length; i++) {
    if (enums[enumId][i].value === enumValue) {
      return enums[enumId][i].label;
    }
  }
  return enumValue;
}

export default enums;
