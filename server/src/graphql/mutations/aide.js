const types = require("../types");
const enums = require("../../enums/aide");
const AideModel = require("../../mongoose/Aide");
const { formatEnumForGraphQL } = require("../../services/enums");
const { permissionDenied, userHasPermission } = require("../../services/user");
const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLInt
} = require("graphql");

module.exports = {
  saveAide: {
    type: types.Aide,
    args: {
      id: { type: GraphQLString },
      auteur: { type: GraphQLString },
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
        type: formatEnumForGraphQL("saveAideStatus", enums.status)
      },
      categorieParticuliere: {
        type: formatEnumForGraphQL(
          "saveAideCategorieParticuliere",
          enums.categorieParticuliere
        )
      },
      demandeTiersPossible: {
        type: GraphQLBoolean
      },
      motsCles: {
        type: GraphQLString
      }
    },
    resolve: async (_, args, context) => {
      // pas d'id : on est en train de créer une nouvelle aide
      let result = null;
      if (!args.id) {
        if (!userHasPermission(context.user, "create_aide")) {
          permissionDenied();
        }
        const aide = new AideModel(args);
        result = await aide.save();
      }

      // un id, c'est une mise à jour
      // on le cherche puis on met à jour si on trouve
      let aide = await AideModel.findById(args.id).populate("auteur");
      if (
        !(
          userHasPermission(context.user, "edit_own_aide", { aide: aide }) ||
          userHasPermission(context.user, "edit_any_aide", { aide: aide })
        )
      ) {
        permissionDenied();
      }
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
      // autoriser l'opération seulement à ceux qui la permission
      // d'effacer leur propre aide ou d'effacer n'importe quelle aide
      let aide = await AideModel.findById(id);
      if (
        !(
          userHasPermission(context.user, "delete_any_aide") ||
          userHasPermission(context.user, "delete_own_aide", { aide })
        )
      ) {
        permissionDenied();
      }
      const result = await AideModel.remove({ _id: id });
      return { id, ...result };
    }
  }
};
