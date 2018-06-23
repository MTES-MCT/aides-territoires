// Déclaration des énumérations, utilisées à la fois pour
// la validation de mongoose et graphQL
module.exports = [
  {
    id: "perimetreApplicationType",
    label: "Échelle",
    values: [
      {
        id: "commune",
        label: "Commune"
      },
      {
        id: "departement",
        label: "Département"
      },
      {
        id: "region",
        label: "Région"
      },
      {
        id: "metropole",
        label: "France métropole et Corse"
      },
      {
        id: "outre_mer",
        label: "Outre mer"
      },
      {
        id: "france",
        label: "France"
      },
      {
        id: "europe",
        label: "Europe"
      }
    ]
  },
  {
    id: "perimetreDiffusionType",
    label: "Périmètre de diffusion",
    values: [
      {
        id: "france",
        label: "France"
      },
      {
        id: "region",
        label: "Région"
      },
      {
        id: "departement",
        label: "Département"
      },
      {
        id: "metropole",
        label: "France métropole et Corse"
      },
      {
        id: "outre_mer",
        label: "Outre mer"
      },
      {
        id: "europe",
        label: "Europe"
      },
      {
        id: "autre",
        label: "Autre"
      }
    ]
  },
  {
    id: "type",
    label: "Type d'aide",
    values: [
      {
        id: "financement",
        label: "Financement"
      },
      {
        id: "ingenierie",
        label: "Ingénierie"
      },
      {
        id: "autre",
        label: "Autre"
      }
    ]
  },
  {
    id: "etape",
    label: "Étape",
    values: [
      {
        id: "pre_operationnel",
        label: "Pré-opérationnel"
      },
      {
        id: "operationnel",
        label: "Opérationnel"
      },
      {
        id: "fonctionnement",
        label: "Fonctionnement"
      },
      {
        id: "autre",
        label: "Autre"
      }
    ]
  },
  {
    id: "statusPublication",
    label: "Statut de publication",
    values: [
      {
        id: "draft",
        label: "Brouillon"
      },
      {
        id: "published",
        label: "Publiée"
      },
      {
        id: "review_required",
        label: "A valider"
      }
    ]
  },
  // subvention, bonification d'intérêt, prêt, avance récupérable,
  // garantie, prêt à taux réduit, investissement en capital, avantage fiscal,
  // fonds de retour, ingenierie de projet, conseil, accompagnement,
  // valorisation, communication
  {
    id: "formeDeDiffusion",
    label: "Modalité de diffusion",
    values: [
      {
        id: "subvention",
        label: "Subvention"
      },
      {
        id: "convention",
        label: "Convention"
      },
      {
        id: "formation",
        label: "Formation"
      },
      {
        id: "bonification_interet",
        label: "Bonification d'intérêt"
      },
      {
        id: "pret",
        label: "prêt"
      },
      {
        id: "avance_recuperable",
        label: "avance récupérable"
      },
      {
        id: "garantie",
        label: "Garantie"
      },
      {
        id: "pret_taux_reduit",
        label: "Prêt à taux réduit"
      },
      {
        id: "investissement_en_capital",
        label: "Investissement en capital"
      },
      {
        id: "avantage_fiscal",
        label: "avantage fiscal"
      },
      {
        id: "fonds_de_retour",
        label: "Fonds de retour"
      },
      {
        id: "ingenierie",
        label: "Ingénierie de projet"
      },
      {
        id: "conseil",
        label: "Conseil"
      },
      {
        id: "accompagnement",
        label: "Accompagnement"
      },
      {
        id: "valorisation",
        label: "Valorisation"
      },
      {
        id: "communication",
        label: "Communication"
      },
      {
        id: "autre",
        label: "Autre"
      }
    ]
  },
  {
    id: "beneficiaires",
    label: "Bénéficiaires",
    values: [
      {
        id: "commune",
        label: "Commune"
      },
      {
        id: "EPCI",
        label: "EPCI"
      },
      {
        id: "entreprises",
        label: "Entreprises"
      },
      {
        id: "societe_civile",
        label: "Société civile"
      },
      {
        id: "associations",
        label: "Associations"
      },
      {
        id: "autre",
        label: "Autre"
      }
    ]
  },
  {
    id: "destination",
    label: "Destination",
    values: [
      {
        id: "etude",
        label: "Etude"
      },
      {
        id: "investissement",
        label: "Investissement"
      },
      {
        id: "fourniture",
        label: "Fourniture"
      },
      {
        id: "fonctionnement",
        label: "Fonctionnement"
      },
      {
        id: "service",
        label: "Service"
      },
      {
        id: "travaux",
        label: "Travaux"
      },
      {
        id: "autre",
        label: "Autre"
      }
    ]
  },
  {
    id: "thematiques",
    label: "Thématiques",
    values: [
      {
        id: "amenagement_durable",
        label: "Aménagement Durable"
      },
      {
        id: "developpement_local",
        label: "Développement local"
      },
      {
        id: "infrastructures_reseaux_et_deplacements",
        label: "Infrastructures, réseaux et déplacements"
      },
      {
        id: "solidarite_et_cohesion_sociale",
        label: "Solidarité et Cohésion sociale"
      }
    ]
  },
  {
    id: "status",
    label: "Calendrier",
    values: [
      {
        id: "ouvert",
        label: "Ouvert"
      },
      {
        id: "projete",
        label: "Projeté"
      },
      {
        id: "ferme",
        label: "Fermé"
      }
    ]
  },
  {
    id: "categorieParticuliere",
    label: "Catégorie particulière",
    values: [
      {
        id: "AAP",
        label: "AAP"
      },
      {
        id: "AMI",
        label: "AMI"
      }
    ]
  }
];
