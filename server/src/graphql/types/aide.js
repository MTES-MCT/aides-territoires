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

const { getEnumAsGraphQLEnumType } = require("../../enumTypes");

const perimetreApplicationType = getEnumAsGraphQLEnumType(
  "PERIMETRE_APPLICATION_TYPES",
  "PERIMETRE_APPLICATION_TYPES"
);

const perimetreDiffusionType = getEnumAsGraphQLEnumType(
  "PERIMETRE_DIFFUSION_TYPES",
  "PERIMETRE_DIFFUSION_TYPES"
);

const aideTypes = getEnumAsGraphQLEnumType("AIDE_TYPES", "AIDE_TYPES");
const aideStatus = getEnumAsGraphQLEnumType("AIDE_STATUS", "AIDE_STATUS");
const aideBeneficiaires = getEnumAsGraphQLEnumType(
  "AIDE_BENEFICIAIRES",
  "AIDE_BENEFICIAIRES"
);
const aideEtapes = getEnumAsGraphQLEnumType("AIDE_ETAPES", "AIDE_ETAPES");

const Aide = new GraphQLObjectType({
  name: "Aide",
  fields: () => ({
    id: { type: GraphQLString },
    name: { type: GraphQLString },
    createdAt: { type: GraphQLString },
    updatedAt: { type: GraphQLString },
    description: { type: GraphQLString },
    criteresEligibilite: { type: GraphQLString },
    type: { type: aideTypes },
    perimetreApplicationType: {
      type: perimetreApplicationType
    },
    perimetreApplicationName: { type: GraphQLString },
    perimetreApplicationCode: { type: GraphQLString },
    perimetreDiffusionType: {
      type: perimetreDiffusionType
    },
    lien: { type: GraphQLString },
    etape: { type: aideEtapes },
    status: { type: aideStatus },
    structurePorteuse: { type: GraphQLString },
    beneficiaires: { type: aideBeneficiaires },
    populationMin: { type: GraphQLInt },
    populationMax: { type: GraphQLInt }
  })
});

Object.assign(module.exports, { Aide });
