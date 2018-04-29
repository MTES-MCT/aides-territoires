// des énumération qui seront utilisées
// pour construire les énumérations de la base de données
// et celles des options possibles pour GraphQL
// ATTENTION, un changement ici impactera donc à la fois mongoose, mongodb
// graphQL

const { GraphQLEnumType } = require("graphql");

const enums = {};

enums.PERIMETRE_APPLICATION_TYPES = {
  label: "type du perimetre d'application",
  description: "les types de territoires sur lesquels l'aide est appliquable",
  enum: [
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
  ]
};

// l'enum PERIMETRE_DIFFUSION_TYPE est le même que le périmètre d'application
enums.PERIMETRE_DIFFUSION_TYPES = {
  label: "type du perimetre de diffusion",
  description: "les types de territoires sur lesquels l'aide est diffusée",
  enum: [
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
  ]
};

enums.AIDE_TYPES = {
  label: "Type d'aide",
  enum: [
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
};

// : ["pre-operationnel", "operationnel", "fonctionnement"]
enums.AIDE_ETAPES = {
  label: "Etape du projet en cours",
  enum: [
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
    }
  ]
};

// ["draft", "published", "review_required", "trash"]
enums.AIDE_STATUS = {
  label: "Status de publication",
  enum: [
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
};

enums.AIDE_BENEFICIAIRES = {
  label: "beneficiaires de l'aide",
  enum: [
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
    }
  ]
};

// transforme un object GraphQLEnumType en un tableau de valeur
// pour mongoose : ['outre_mer', 'europe']
exports.getEnumAsArray = typeName => {
  return enums[typeName].enum.map(v => v.value);
};

exports.getEnumAsGraphQLEnumType = (name, typeName) => {
  const enumType = enums[typeName];
  const graphQLType = {
    name: name,
    description: enumType.description ? enumType.description : enumType.name,
    values: {}
  };
  enumType.enum.map(data => {
    graphQLType.values[data.value] = {
      value: data.value,
      departement: data.label
    };
  });
  return new GraphQLEnumType(graphQLType);
  //return GraphQLEnumType.getValues().map(v => v.value);
};

exports.enums = enums;
