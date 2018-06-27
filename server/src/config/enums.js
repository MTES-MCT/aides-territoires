// Déclaration des énumérations, utilisées à la fois pour
// la validation de mongoose et graphQL
// !!! @todo utiliser "id" pour les values peut rendre confus le cache client d'apollo
// qui va partir du principe qu'un id ne peut existe qu'une seule fois à travers
// l'ensemble de toutes les values du site. Or il est possible d'avoir deux
// values "autre" dans deux enums différents.
module.exports = [
  {
    id: "perimetreApplicationType",
    label: "Échelle",
    values: [
      {
        id: "commune",
        label: "Commune",
        description: ""
      },
      {
        id: "departement",
        label: "Département",
        description: ""
      },
      {
        id: "region",
        label: "Région",
        description: ""
      },
      {
        id: "metropole",
        label: "France métropole et Corse",
        description: ""
      },
      {
        id: "outre_mer",
        label: "Outre mer",
        description: ""
      },
      {
        id: "france",
        label: "France",
        description: ""
      },
      {
        id: "europe",
        label: "Europe",
        description: ""
      }
    ]
  },
  {
    id: "perimetreDiffusionType",
    label: "Périmètre de diffusion",
    values: [
      {
        id: "france",
        label: "France",
        description: ""
      },
      {
        id: "region",
        label: "Région",
        description: ""
      },
      {
        id: "departement",
        label: "Département",
        description: ""
      },
      {
        id: "metropole",
        label: "France métropole et Corse",
        description: ""
      },
      {
        id: "outre_mer",
        label: "Outre mer",
        description: ""
      },
      {
        id: "europe",
        label: "Europe",
        description: ""
      },
      {
        id: "autre",
        label: "Autre",
        description: ""
      }
    ]
  },
  {
    id: "type",
    label: "Type d'aide",
    values: [
      {
        id: "financement",
        label: "Financement",
        description: ""
      },
      {
        id: "autre",
        label: "Non financier",
        description: ""
      }
    ]
  },
  {
    id: "etape",
    label: "Quand mobiliser l'aide ?",
    values: [
      {
        id: "pre_operationnel",
        label: "Pré-opérationnel",
        description: ""
      },
      {
        id: "operationnel",
        label: "Opérationnel",
        description: ""
      },
      {
        id: "fonctionnement",
        label: "Fonctionnement",
        description: ""
      }
    ]
  },
  {
    id: "statusPublication",
    label: "Statut de publication",
    values: [
      {
        id: "draft",
        label: "Brouillon",
        description: ""
      },
      {
        id: "published",
        label: "Publiée",
        description: ""
      },
      {
        id: "review_required",
        label: "A valider",
        description: ""
      }
    ]
  },
  // subvention, bonification d'intérêt, prêt, avance récupérable,
  // garantie, prêt à taux réduit, investissement en capital, avantage fiscal,
  // fonds de retour, ingenierie de projet, conseil, accompagnement,
  // valorisation, communication
  {
    id: "formeDeDiffusion",
    label: "Nature de l'aide",
    values: [
      {
        id: "subvention",
        label: "Subvention",
        description: ""
      },
      {
        id: "convention",
        label: "Convention",
        description: ""
      },
      {
        id: "formation",
        label: "Formation",
        description: ""
      },
      {
        id: "bonification_interet",
        label: "Bonification d'intérêt",
        description: ""
      },
      {
        id: "pret",
        label: "prêt",
        description: ""
      },
      {
        id: "avance_recuperable",
        label: "avance récupérable",
        description: ""
      },
      {
        id: "garantie",
        label: "Garantie",
        description: ""
      },
      {
        id: "pret_taux_reduit",
        label: "Prêt à taux réduit",
        description: ""
      },
      {
        id: "investissement_en_capital",
        label: "Investissement en capital",
        description: ""
      },
      {
        id: "avantage_fiscal",
        label: "avantage fiscal",
        description: ""
      },
      {
        id: "fonds_de_retour",
        label: "Fonds de retour",
        description: ""
      },
      {
        id: "ingenierie",
        label: "Ingénierie de projet",
        description: ""
      },
      {
        id: "conseil",
        label: "Conseil",
        description: ""
      },
      {
        id: "accompagnement",
        label: "Accompagnement",
        description: ""
      },
      {
        id: "valorisation",
        label: "Valorisation",
        description: ""
      },
      {
        id: "communication",
        label: "Communication",
        description: ""
      },
      {
        id: "autre",
        label: "Autre",
        description: ""
      }
    ]
  },
  {
    id: "beneficiaires",
    label: "Public visé",
    values: [
      {
        id: "commune",
        label: "Commune",
        description: ""
      },
      {
        id: "departement",
        label: "Département",
        description: ""
      },
      {
        id: "region",
        label: "Région",
        description: ""
      },
      {
        id: "EPCI",
        label: "EPCI",
        description: ""
      },
      {
        id: "entreprises",
        label: "Entreprises",
        description: ""
      },
      {
        id: "societe_civile",
        label: "Société civile",
        description: ""
      },
      {
        id: "associations",
        label: "Associations",
        description: ""
      },
      {
        id: "autre",
        label: "Autre",
        description: ""
      }
    ]
  },
  {
    id: "destination",
    label: "Destination de l'aide",
    values: [
      {
        id: "etude",
        label: "Etude",
        description: ""
      },
      {
        id: "investissement",
        label: "Investissement",
        description: ""
      },
      {
        id: "fourniture",
        label: "Fourniture",
        description: ""
      },
      {
        id: "fonctionnement",
        label: "Fonctionnement",
        description: ""
      },
      {
        id: "service",
        label: "Service",
        description: ""
      },
      {
        id: "travaux",
        label: "Travaux",
        description: ""
      },
      {
        id: "autre",
        label: "Autre",
        description: ""
      }
    ]
  },
  {
    id: "thematiques",
    label: "Thématiques",
    values: [
      {
        id: "amenagement_durable",
        label: "Aménagement Durable",
        description: ""
      },
      {
        id: "developpement_local",
        label: "Développement local",
        description: ""
      },
      {
        id: "infrastructures_reseaux_et_deplacements",
        label: "Infrastructures, réseaux et déplacements",
        description: ""
      },
      {
        id: "solidarite_et_cohesion_sociale",
        label: "Solidarité et Cohésion sociale",
        description: ""
      }
    ]
  },
  {
    id: "status",
    label: "Calendrier",
    values: [
      {
        id: "ouvert",
        label: "Ouvert",
        description: ""
      },
      {
        id: "projete",
        label: "Projeté",
        description: ""
      },
      {
        id: "ferme",
        label: "Fermé",
        description: ""
      }
    ]
  },
  {
    id: "categorieParticuliere",
    label: "Catégorie particulière",
    values: [
      {
        id: "AAP",
        label: "AAP",
        description: ""
      },
      {
        id: "AMI",
        label: "AMI",
        description: ""
      }
    ]
  }
];
