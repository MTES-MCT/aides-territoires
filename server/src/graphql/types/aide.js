module.exports = {};
const enums = require("../../enums/aide");
const { formatEnumForGraphQL } = require("../../services/enums");
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

const Aide = new GraphQLObjectType({
  name: "Aide",
  fields: () => ({
    id: { type: GraphQLString },
    nom: { type: GraphQLString },
    createdAt: { type: GraphQLString },
    updatedAt: { type: GraphQLString },
    description: { type: GraphQLString },
    criteresEligibilite: { type: GraphQLString },
    type: { type: GraphQLString },
    perimetreApplicationType: {
      type: GraphQLString
    },
    perimetreApplicationNom: { type: GraphQLString },
    perimetreApplicationCode: { type: GraphQLString },
    perimetreDiffusionType: {
      type: GraphQLString
    },
    perimetreDiffusionTypeAutre: { type: GraphQLString },
    lien: { type: GraphQLString },
    etape: { type: formatEnumForGraphQL("etape", enums.etape) },
    statusPublication: { type: GraphQLString },
    structurePorteuse: { type: GraphQLString },
    beneficiaires: {
      type: formatEnumForGraphQL("beneficiaires", enums.beneficiaires)
    },
    beneficiairesAutre: {
      type: GraphQLString
    },
    destination: {
      type: formatEnumForGraphQL("destination", enums.destination)
    },
    populationMin: { type: GraphQLInt },
    populationMax: { type: GraphQLInt },
    formeDeDiffusion: {
      type: formatEnumForGraphQL("formeDeDiffusion", enums.formeDeDiffusion)
    },
    thematiques: {
      type: formatEnumForGraphQL("thematiques", enums.thematiques)
    },
    dateEcheance: {
      type: GraphQLString
    },
    tauxSubvention: {
      type: GraphQLString
    },
    contact: {
      type: GraphQLString
    },
    status: {
      type: GraphQLString
    }
  })
});

Object.assign(module.exports, { Aide });
