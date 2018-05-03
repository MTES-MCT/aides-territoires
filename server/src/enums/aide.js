// Déclaration des énumérations, utilisées à la fois pour
// la validation de mongoose et graphQL
module.exports = {
  perimetreApplicationType: [
    {
      value: "commune",
      label: "Commune"
    },
    {
      value: "departement",
      label: "Département"
    },
    {
      value: "region",
      label: "Région"
    },
    {
      value: "metropole",
      label: "France métropole et Corse"
    },
    {
      value: "outre_mer",
      label: "Outre mer"
    },
    {
      value: "france",
      label: "France"
    },
    {
      value: "europe",
      label: "Europe"
    }
  ],
  perimetreDiffusionType: [
    {
      value: "france",
      label: "France"
    },
    {
      value: "region",
      label: "Région"
    },
    {
      value: "departement",
      label: "Département"
    },
    {
      value: "metropole",
      label: "France métropole et Corse"
    },
    {
      value: "outre_mer",
      label: "Outre mer"
    },
    {
      value: "europe",
      label: "Europe"
    },
    {
      value: "autre",
      label: "Autre"
    }
  ],
  type: [
    {
      value: "financement",
      label: "Financement"
    },
    {
      value: "ingenierie",
      label: "Ingénierie"
    },
    {
      value: "autre",
      label: "Autre"
    }
  ],
  etape: [
    {
      value: "pre_operationnel",
      label: "Pré-opérationnel"
    },
    {
      value: "operationnel",
      label: "Opérationnel"
    },
    {
      value: "fonctionnement",
      label: "Fonctionnement"
    },
    {
      value: "autre",
      label: "Autre"
    }
  ],
  statusPublication: [
    {
      value: "draft",
      label: "Brouillon"
    },
    {
      value: "published",
      label: "Publiée"
    },
    {
      value: "review_required",
      label: "A valider"
    }
  ],
  // subvention, bonification d'intérêt, prêt, avance récupérable,
  // garantie, prêt à taux réduit, investissement en capital, avantage fiscal,
  // fonds de retour, ingenierie de projet, conseil, accompagnement,
  // valorisation, communication
  formeDeDiffusion: [
    {
      value: "subvention",
      label: "Subvention"
    },
    {
      value: "bonification_interet",
      label: "Bonification d'intérêt"
    },
    {
      value: "pret",
      label: "prêt"
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
      value: "pret_taux_reduit",
      label: "Prêt à taux réduit"
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
      value: "ingenierie",
      label: "Ingénierie de projet"
    },
    {
      value: "conseil",
      label: "Conseil"
    },
    {
      value: "accompagnement",
      label: "Accompagnement"
    },
    {
      value: "valorisation",
      label: "Valorisation"
    },
    {
      value: "communication",
      label: "Communication"
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
      value: "etude",
      label: "Etude"
    },
    {
      value: "investissement",
      label: "Investissement"
    },
    {
      value: "fourniture",
      label: "Fourniture"
    },
    {
      value: "fonctionnement",
      label: "Fonctionnement"
    },
    {
      value: "service",
      label: "Service"
    },
    {
      value: "travaux",
      label: "Travaux"
    }
  ]
};
