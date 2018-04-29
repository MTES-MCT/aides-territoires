const types = require("../types");
const AideModel = require("../../mongoose/Aide");
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLList,
  GraphQLInt
} = require("graphql");

const { getEnumAsGraphQLEnumType } = require("../../enumTypes");

const perimetreApplicationType = getEnumAsGraphQLEnumType(
  "filter_perimetreApplicationType",
  "PERIMETRE_APPLICATION_TYPES"
);

const perimetreDiffusionType = getEnumAsGraphQLEnumType(
  "filter_perimetreDiffusionType",
  "PERIMETRE_DIFFUSION_TYPES"
);

const aideTypes = getEnumAsGraphQLEnumType("filter_aide_type", "AIDE_TYPES");
const aideStatus = getEnumAsGraphQLEnumType(
  "filter_aide_status",
  "AIDE_STATUS"
);
const aideBeneficiaires = getEnumAsGraphQLEnumType(
  "filter_aide_beneficaires",
  "AIDE_BENEFICIAIRES"
);
const aideEtapes = getEnumAsGraphQLEnumType(
  "filter_aide_etapes",
  "AIDE_ETAPES"
);

module.exports = {
  saveAide: {
    type: types.Aide,
    args: {
      id: { type: GraphQLString },
      name: { type: GraphQLString },
      createdAt: { type: GraphQLString },
      updatedAt: { type: GraphQLString },
      description: { type: GraphQLString },
      criteresEligibilite: { type: GraphQLString },
      type: { type: new GraphQLList(aideTypes) },
      perimetreApplicationType: {
        type: perimetreApplicationType
      },
      perimetreApplicationName: { type: GraphQLString },
      perimetreApplicationCode: { type: GraphQLString },
      perimetreDiffusionType: {
        type: new GraphQLList(perimetreDiffusionType)
      },
      lien: { type: GraphQLString },
      etape: { type: new GraphQLList(aideEtapes) },
      status: { type: new GraphQLList(aideStatus) },
      structurePorteuse: { type: GraphQLString },
      beneficiaires: { type: new GraphQLList(aideBeneficiaires) },
      populationMin: { type: GraphQLInt },
      populationMax: { type: GraphQLInt }
    },
    resolve: async (_, args, context) => {
      // pas d'id : on créer une nouvelle aide
      let result = null;
      if (!args.id) {
        const aide = new AideModel(args);
        result = await aide.save();
      }
      // un id, on le cherche puis on met à jour si on trouve
      let aide = await AideModel.findById(args.id);
      if (aide) {
        aide = Object.assign(aide, args);
        result = aide.save();
      }
      return result;
    }
  },
  deleteAide: {
    type: new GraphQLObjectType({
      name: "deleteAide",
      fields: () => ({
        id: { type: GraphQLString },
        n: { type: GraphQLString },
        ok: { type: GraphQLString }
      })
    }),
    args: {
      id: {
        type: GraphQLID
      }
    },
    resolve: async (_, { id }, context) => {
      const result = await AideModel.remove({ _id: id });
      return { id, ...result };
    }
  }
};
