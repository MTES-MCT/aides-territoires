// Déclaration des énumérations, utilisées à la fois pour
// la validation de mongoose et graphQL
module.exports = [
  {
    id: "perimetreApplicationType",
    label: "Échelle",
    options: [
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
    ]
  },
  {
    id: "perimetreDiffusionType",
    label: "Périmètre de diffusion",
    options: [
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
    ]
  },
  {
    id: "type",
    label: "Type d'aide",
    options: [
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
    ]
  },
  {
    id: "etape",
    label: "Étape",
    options: [
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
    ]
  },
  {
    id: "statusPublication",
    label: "Statut de publication",
    options: [
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
    ]
  },
  // subvention, bonification d'intérêt, prêt, avance récupérable,
  // garantie, prêt à taux réduit, investissement en capital, avantage fiscal,
  // fonds de retour, ingenierie de projet, conseil, accompagnement,
  // valorisation, communication
  {
    id: "formeDeDiffusion",
    label: "Modalité de diffusion",
    options: [
      {
        value: "subvention",
        label: "Subvention"
      },
      {
        value: "convention",
        label: "Convention"
      },
      {
        value: "formation",
        label: "Formation"
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
      },
      {
        value: "autre",
        label: "Autre"
      }
    ]
  },
  {
    id: "beneficiaires",
    label: "Bénéficiaires",
    options: [
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
        value: "societe_civile",
        label: "Société civile"
      },
      {
        value: "associations",
        label: "Associations"
      },
      {
        value: "autre",
        label: "Autre"
      }
    ]
  },
  {
    id: "destination",
    label: "Destination",
    options: [
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
      },
      {
        value: "autre",
        label: "Autre"
      }
    ]
  },
  {
    id: "thematiques",
    label: "Thématiques",
    options: [
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
    ]
  },
  {
    id: "status",
    label: "Calendrier",
    options: [
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
    ]
  },
  {
    id: "categorieParticuliere",
    label: "Catégorie particulière",
    options: [
      {
        value: "AAP",
        label: "AAP"
      },
      {
        value: "AMI",
        label: "AMI"
      }
    ]
  }
];
