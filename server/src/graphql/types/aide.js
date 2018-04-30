module.exports = {};

const {
  GraphQLID,
  GraphQLObjectType,
  GraphQLNonNull,
  GraphQLEnumType,
  GraphQLInt,
  GraphQLString,
  GraphQLBoolean,
  GraphQLList
} = require("graphql");

const { enums, formatEnumForGraphQL } = require("../../enums");

const perimetreApplicationType = formatEnumForGraphQL(
  "perimetreApplicationType",
  enums.AIDE_PERIMETRE_APPLICATION_TYPES
);

const perimetreDiffusionTypes = formatEnumForGraphQL(
  "perimetreDiffusionType",
  enums.AIDE_PERIMETRE_DIFFUSION_TYPES
);

const aideTypes = formatEnumForGraphQL("aideTypes", enums.AIDE_TYPES);
const statusPublication = formatEnumForGraphQL(
  "statusPublication",
  enums.AIDE_STATUS_PUBLICATION
);
const aideBeneficiaires = formatEnumForGraphQL(
  "beneficiaires",
  enums.AIDE_BENEFICIAIRES
);
const aideEtapes = formatEnumForGraphQL("aideEtapes", enums.AIDE_ETAPES);

const Aide = new GraphQLObjectType({
  name: "Aide",
  fields: () => ({
    id: { type: GraphQLString },
    nom: { type: GraphQLString },
    createdAt: { type: GraphQLString },
    updatedAt: { type: GraphQLString },
    description: { type: GraphQLString },
    criteresEligibilite: { type: GraphQLString },
    type: { type: aideTypes },
    perimetreApplicationType: {
      type: perimetreApplicationType
    },
    perimetreApplicationNom: { type: GraphQLString },
    perimetreApplicationCode: { type: GraphQLString },
    perimetreDiffusionType: {
      type: perimetreDiffusionTypes
    },
    lien: { type: GraphQLString },
    etape: { type: aideEtapes },
    statusPublication: { type: statusPublication },
    structurePorteuse: { type: GraphQLString },
    beneficiaires: { type: new GraphQLList(GraphQLString) },
    populationMin: { type: GraphQLInt },
    populationMax: { type: GraphQLInt }
  })
});

Object.assign(module.exports, { Aide });
