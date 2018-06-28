const types = require("../types");
const AideModel = require("../../mongoose/Aide");
const { getEnumByIdForGraphQL } = require("../../services/enums");
const {
  permissionDenied,
  userHasPermission,
  notifyRoleByEmail,
  userHasRole
} = require("../../services/user");
const { getAide } = require("../../services/aide");
const config = require("../../../config");

const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLInt,
  GraphQLList
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
        type: GraphQLList(getEnumByIdForGraphQL("saveAideEtape", "etape"))
      },
      statusPublication: { type: GraphQLString },
      structurePorteuse: { type: GraphQLString },
      formeDeDiffusionAutre: { type: GraphQLString },
      beneficiaires: {
        type: GraphQLList(
          getEnumByIdForGraphQL("saveAideBeneficiaires", "beneficiaires")
        )
      },
      beneficiairesAutre: { type: GraphQLString },
      destination: {
        type: GraphQLList(
          getEnumByIdForGraphQL("saveAideDestination", "destination")
        )
      },
      destinationAutre: { type: GraphQLString },
      populationMin: { type: GraphQLInt },
      populationMax: { type: GraphQLInt },
      formeDeDiffusion: {
        type: GraphQLList(
          getEnumByIdForGraphQL("saveAideFormeDeDiffusion", "formeDeDiffusion")
        )
      },
      thematiques: {
        type: GraphQLList(
          getEnumByIdForGraphQL("saveAideThematiques", "thematiques")
        )
      },
      dateEcheance: {
        type: GraphQLString
      },
      dateDebut: {
        type: GraphQLString
      },
      datePredepot: {
        type: GraphQLString
      },
      tauxSubvention: {
        type: GraphQLString
      },
      contact: {
        type: GraphQLString
      },
      status: {
        type: getEnumByIdForGraphQL("saveAideStatus", "status")
      },
      categorieParticuliere: {
        type: GraphQLList(
          getEnumByIdForGraphQL(
            "saveAideCategorieParticuliere",
            "categorieParticuliere"
          )
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
      // CREATION D'UNE NOUVELLE AIDE
      if (!args.id) {
        if (!userHasPermission(context.user, "create_aide")) {
          permissionDenied();
        }
        const aide = new AideModel(args);
        // si la personne n'a pas la permission de de publier, on
        // force la publication en "review_required"
        if (!userHasPermission(context.user, "publish_aide")) {
          aide.statusPublication = "review_required";
        }
        result = await aide.save();
        if (userHasRole(context.user, "contributeur")) {
          notifyRoleByEmail("admin", {
            subject: "Aides-territoires - nouvelle aide : " + aide.nom,
            text: `Bonjour, une nouvelle aide a été créée sur aides-territoires.<br /> 
          Vous pouvez la consulter en <a href="${
            config.aidesTerritoiresUrl
          }/admin/aide/${aide.id}/edit">cliquant sur ce lien.</a>`
          });
        }
      }

      // EDITION D'UNE AIDE EXISTANTE
      // un id, c'est une mise à jour
      // on le cherche puis on met à jour si on trouve
      let aide = await getAide(args.id);
      if (
        !(
          userHasPermission(context.user, "edit_own_aide", { aide: aide }) ||
          userHasPermission(context.user, "edit_any_aide")
        )
      ) {
        permissionDenied();
      }
      if (aide) {
        const previousStatusPublication = aide.statusPublication;
        aide = Object.assign(aide, args);
        // si la personne n'a pas la permission de de publier, on
        // force la publication en "review_required", sauf il l'aide
        // est déjà publiée
        if (!userHasPermission(context.user, "publish_aide")) {
          if (previousStatusPublication.statusPublication !== "published") {
            aide.statusPublication = "review_required";
          }
        }
        result = aide.save();
        if (userHasRole(context.user, "contributeur")) {
          notifyRoleByEmail("admin", {
            subject: "Aides-territoires - édition d'une aide : " + aide.nom,
            text: `Bonjour, une aide a été édité sur aides-territoires.<br /> 
          Vous pouvez la consulter en <a href="${
            config.aidesTerritoiresUrl
          }/admin/aide/${aide.id}/edit">cliquant sur ce lien.</a>`
          });
        }
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
      let aide = await getAide(id);
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
