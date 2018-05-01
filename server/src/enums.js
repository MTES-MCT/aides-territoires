// des énumération qui seront utilisées
// pour construire les énumérations de la base de données
// et celles des options possibles pour GraphQL
// ATTENTION, un changement ici impactera donc à la fois mongoose, mongodb
// graphQL
const logger = require("./services/logger");
const { GraphQLEnumType } = require("graphql");

const enums = {};

enums.AIDE_PERIMETRE_APPLICATION_TYPES = [
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
];

// l'enum PERIMETRE_DIFFUSION_TYPE est le même que le périmètre d'application
enums.AIDE_PERIMETRE_DIFFUSION_TYPES = [
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
  }
];

enums.AIDE_TYPES = [
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
];

// : ["pre-operationnel", "operationnel", "fonctionnement"]
enums.AIDE_ETAPES = [
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
];

// ["draft", "published", "review_required", "trash"]
enums.AIDE_STATUS_PUBLICATION = [
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
];

enums.AIDE_BENEFICIAIRES = [
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
];

exports.formatEnumForMongoose = enumType => {
  return enumType.map(r => r.value);
};

exports.formatEnumForGraphQL = (graphQLName, enumType) => {
  if (!enumType) {
    logger.error(
      "fonction formatEnumForGraphQL : L'énumération n'est pas définie pour " +
        graphQLName
    );
  }
  const graphQLType = {
    name: graphQLName,
    values: {}
  };
  enumType.map(data => {
    graphQLType.values[data.value] = {
      value: data.value,
      departement: data.label
    };
  });
  return new GraphQLEnumType(graphQLType);
};

exports.enums = enums;
