module.exports = {};
const types = require("../types");
const { getEnumByIdForGraphQL } = require("../../services/enums");
const {
  GraphQLObjectType,
  GraphQLList,
  GraphQLInt,
  GraphQLString,
  GraphQLBoolean
} = require("graphql");

const Aide = new GraphQLObjectType({
  name: "Aide",
  fields: () => ({
    id: { type: GraphQLString },
    auteur: { type: types.User },
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
    etape: { type: GraphQLList(getEnumByIdForGraphQL("aideEtape", "etape")) },
    statusPublication: { type: GraphQLString },
    structurePorteuse: { type: GraphQLString },
    beneficiaires: {
      type: GraphQLList(
        getEnumByIdForGraphQL("aideBeneficiaires", "beneficiaires")
      )
    },
    beneficiairesAutre: {
      type: GraphQLString
    },
    destination: {
      type: GraphQLList(getEnumByIdForGraphQL("aideDestination", "destination"))
    },
    destinationAutre: { type: GraphQLString },
    populationMin: { type: GraphQLInt },
    populationMax: { type: GraphQLInt },
    formeDeDiffusion: {
      type: GraphQLList(
        getEnumByIdForGraphQL("aideFormeDeDiffusion", "formeDeDiffusion")
      )
    },
    formeDeDiffusionAutre: { type: GraphQLString },
    thematiques: {
      type: new GraphQLList(
        getEnumByIdForGraphQL("aideThematiques", "thematiques")
      )
    },
    dateEcheance: {
      type: GraphQLString
    },
    dateDebut: {
      type: GraphQLString
    },
    tauxSubvention: {
      type: GraphQLString
    },
    contact: {
      type: GraphQLString
    },
    status: {
      type: getEnumByIdForGraphQL("aideStatus", "status")
    },
    motsCles: {
      type: GraphQLString
    },
    categorieParticuliere: {
      type: GraphQLList(
        getEnumByIdForGraphQL(
          "aideCategorieParticuliere",
          "categorieParticuliere"
        )
      )
    },
    demandeTiersPossible: {
      type: GraphQLBoolean
    }
  })
});

Object.assign(module.exports, { Aide });
