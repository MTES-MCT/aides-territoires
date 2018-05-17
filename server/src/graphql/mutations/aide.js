const types = require("../types");
const enums = require("../../enums/aide");
const AideModel = require("../../mongoose/Aide");
const { formatEnumForGraphQL } = require("../../services/enums");
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLList,
  GraphQLInt
} = require("graphql");

module.exports = {
  saveAide: {
    type: types.Aide,
    args: {
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
      perimetreDiffusionTypeAutre: {
        type: GraphQLString
      },
      lien: { type: GraphQLString },
      etape: {
        type: formatEnumForGraphQL("saveAideEtape", enums.etape)
      },
      statusPublication: { type: GraphQLString },
      structurePorteuse: { type: GraphQLString },
      formeDeDiffusion: { type: GraphQLString },
      formeDeDiffusionAutre: { type: GraphQLString },
      beneficiaires: {
        type: formatEnumForGraphQL("saveAideBeneficiaires", enums.beneficiaires)
      },
      beneficiairesAutre: { type: GraphQLString },
      destination: {
        type: formatEnumForGraphQL("saveAideDestination", enums.destination)
      },
      destinationAutre: { type: GraphQLString },
      populationMin: { type: GraphQLInt },
      populationMax: { type: GraphQLInt },
      formeDeDiffusion: {
        type: formatEnumForGraphQL(
          "saveAideFormeDeDiffusion",
          enums.formeDeDiffusion
        )
      },
      thematiques: {
        type: formatEnumForGraphQL("saveAideThematiques", enums.thematiques)
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
        type: formatEnumForGraphQL("saveAideStatus", enums.status)
      }
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
