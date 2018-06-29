const types = require("../types");
const { getEnumByIdForGraphQL } = require("../../services/enums");
const {
  GraphQLObjectType,
  GraphQLInputObjectType,
  GraphQLString,
  GraphQLID,
  GraphQLBoolean,
  GraphQLList,
  GraphQLInt,
  GraphQLEnumType
} = require("graphql");

const { searchAides, getAides, getAide } = require("../../services/aide");
const { userHasPermission } = require("../../services/user");

const searchAideTypeDeTerritoireType = new GraphQLObjectType({
  name: "searchAideTypesDeTerritoires",
  fields: {
    type: { type: GraphQLString },
    label: { type: GraphQLString },
    aides: { type: new GraphQLList(types.Aide) }
  }
});

const searchAideResultsGroupType = new GraphQLObjectType({
  name: "searchAideResultsGroup",
  fields: {
    nombreAides: { type: GraphQLInt },
    type: { type: GraphQLString },
    label: { type: GraphQLString },
    aidesParTypeDeTerritoires: {
      type: new GraphQLList(searchAideTypeDeTerritoireType)
    }
  }
});

module.exports = {
  getAide: {
    type: new GraphQLObjectType({
      name: "getAide",
      fields: {
        meta: {
          type: new GraphQLObjectType({
            name: "getAideMeta",
            fields: {
              userUiPermissions: { type: new GraphQLList(GraphQLString) }
            }
          })
        },
        node: { type: types.Aide }
      }
    }),
    args: {
      id: {
        type: GraphQLID
      }
    },
    resolve: async (_, { id }) => {
      return await {
        meta: {
          userUiPermissions: []
        },
        node: getAide(id)
      };
    }
  },
  /**
   * La query utilisée pour retournée les aides du moteur de recherche,
   * groupées par localisations
   */
  rechercheAides: {
    type: new GraphQLObjectType({
      name: "searchAidesResults",
      fields: {
        totalNombreAides: { type: GraphQLInt },
        groupesDeResultats: {
          type: new GraphQLList(searchAideResultsGroupType)
        }
      }
    }),
    args: {
      filters: {
        type: new GraphQLInputObjectType({
          name: "searchAidesFilters",
          fields: {
            auteur: {
              type: GraphQLString
            },
            etape: {
              type: new GraphQLList(
                getEnumByIdForGraphQL("searchAidesEtape", "etape")
              )
            },
            statusPublication: {
              type: new GraphQLList(
                getEnumByIdForGraphQL(
                  "searchAidesStatusPublication",
                  "statusPublication"
                )
              )
            },
            type: {
              type: new GraphQLList(
                getEnumByIdForGraphQL("searchAidesType", "type")
              )
            },
            // texte entré pour la recherche libre (par mots clefs)
            texte: {
              type: GraphQLString
            },
            // le perimetre initial de recherche: ex: département
            typePerimetreInitialDeRecherche: {
              type: getEnumByIdForGraphQL(
                "searchAidesTypePerimetreInitialDeRecherche",
                "perimetreApplicationType"
              )
            },
            // le code insee ou identifiant unique associé au périmètre de recherche
            // ex : 44 pour le typeDeperimetreInitialDeRecherche "Loire-Atlantique"
            // en croisant le type
            codePerimetreInitialDeRecherche: {
              type: GraphQLString
            },
            // le perimetre d'application enregistré pour l'aide
            // (département, région, EPCI, etc)
            perimetreApplicationType: {
              type: new GraphQLList(
                getEnumByIdForGraphQL(
                  "searchAidesPerimetreApplicationType",
                  "perimetreApplicationType"
                )
              )
            },
            destination: {
              type: new GraphQLList(
                getEnumByIdForGraphQL("searchAidesDestination", "destination")
              )
            },
            destinationAutre: {
              type: GraphQLString
            },
            formeDeDiffusionAutre: {
              type: GraphQLString
            },
            beneficiaires: {
              type: new GraphQLList(
                getEnumByIdForGraphQL(
                  "searchAidesBeneficiaires",
                  "beneficiaires"
                )
              )
            },
            perimetreApplicationCode: {
              type: GraphQLString
            },
            formeDeDiffusion: {
              type: new GraphQLList(
                getEnumByIdForGraphQL(
                  "searchAidesFormeDeDiffusion",
                  "formeDeDiffusion"
                )
              )
            },
            thematiques: {
              type: new GraphQLList(
                getEnumByIdForGraphQL("searchAidesThematiques", "thematiques")
              )
            },
            status: {
              type: GraphQLString
            },
            categorieParticuliere: {
              type: new GraphQLList(GraphQLString)
            },
            demandeTiersPossible: {
              type: GraphQLBoolean
            },
            motsCles: {
              type: GraphQLString
            },
            codeDepartement: {
              type: GraphQLString
            },
            dateEcheance: {
              type: new GraphQLInputObjectType({
                name: "rechercheAidesDateEcheance",
                fields: {
                  operator: {
                    type: new GraphQLEnumType({
                      name: "rechercheAidesDateEcheanceOperator",
                      values: {
                        eq: { value: "eq" },
                        lt: { value: "lt" },
                        gt: { value: "gt" },
                        lte: { value: "lte" },
                        gte: { value: "gte" }
                      }
                    })
                  },
                  value: { type: GraphQLString }
                }
              })
            },
            datePredepot: {
              type: new GraphQLInputObjectType({
                name: "rechercheAidesDatePreDepot",
                fields: {
                  operator: {
                    type: new GraphQLEnumType({
                      name: "rechercheAidesDatePreDepotOperators",
                      values: {
                        eq: { value: "eq" },
                        lt: { value: "lt" },
                        gt: { value: "gt" },
                        lte: { value: "lte" },
                        gte: { value: "gte" }
                      }
                    })
                  },
                  value: { type: GraphQLString }
                }
              })
            }
          }
        })
      }
    },
    resolve: async (_, { filters = {}, sort }, context) => {
      return searchAides(filters, { sort, context });
    }
  },
  allAides: {
    type: new GraphQLObjectType({
      name: "allAides",
      fields: {
        edges: {
          type: new GraphQLList(
            new GraphQLObjectType({
              name: "allAideEdges",
              fields: {
                meta: {
                  type: new GraphQLObjectType({
                    name: "allAidesEdgesMeta",
                    fields: {
                      userUiPermissions: {
                        type: new GraphQLList(GraphQLString)
                      }
                    }
                  })
                },
                node: { type: types.Aide }
              }
            })
          )
        }
      }
    }),
    args: {
      sort: {
        type: new GraphQLEnumType({
          name: "allAidesSort",
          values: {
            updatedAtDesc: {
              value: "-updatedAt"
            },
            updatedAtAsc: {
              value: "updatedAt"
            },
            createdAtDesc: {
              value: "-updatedAt"
            },
            createdAtAsc: {
              value: "updatedAt"
            }
          }
        })
      },
      filters: {
        type: new GraphQLInputObjectType({
          name: "allAidesFilters",
          fields: {
            fullTextSearch: {
              type: GraphQLString
            },
            auteur: { type: GraphQLID },
            etape: {
              type: new GraphQLList(
                getEnumByIdForGraphQL("allAidesEtape", "etape")
              )
            },
            statusPublication: {
              type: getEnumByIdForGraphQL(
                "allAidesStatusPublication",
                "statusPublication"
              )
            },
            type: {
              type: new GraphQLList(
                getEnumByIdForGraphQL("allAidesType", "type")
              )
            },
            perimetreApplicationType: {
              type: new GraphQLList(
                getEnumByIdForGraphQL(
                  "allAidesPerimetreApplicationType",
                  "perimetreApplicationType"
                )
              )
            },
            destination: {
              type: new GraphQLList(
                getEnumByIdForGraphQL("allAidesDestination", "destination")
              )
            },
            destinationAutre: {
              type: GraphQLString
            },
            formeDeDiffusionAutre: {
              type: GraphQLString
            },
            beneficiaires: {
              type: new GraphQLList(
                getEnumByIdForGraphQL("allAidesBeneficiaires", "beneficiaires")
              )
            },
            perimetreApplicationCode: {
              type: GraphQLString
            },
            formeDeDiffusion: {
              type: new GraphQLList(
                getEnumByIdForGraphQL(
                  "allAidesFormeDeDiffusion",
                  "formeDeDiffusion"
                )
              )
            },
            thematiques: {
              type: new GraphQLList(
                getEnumByIdForGraphQL("allAidesThematiques", "thematiques")
              )
            },
            status: {
              type: GraphQLString
            },
            categorieParticuliere: {
              type: GraphQLString
            },
            demandeTiersPossible: {
              type: GraphQLBoolean
            },
            motsCles: {
              type: GraphQLString
            }
          }
        })
      }
    },
    resolve: async (_, { filters, sort = "-updatedAt" }, context) => {
      const aides = await getAides(filters, {
        sort,
        showUnpublished: true,
        context
      });
      // ajouter les permission : l'utilisateur peut voir les boutons
      // effacer et éditer seulement si il a les permission ci-dessous
      const edges = aides.map(aide => {
        // envoyer des informations au front pour savoir si l'utilisateur
        // à le droit de voir le bouton éditer, effacer, clone, en fonction de
        // l'aide (les droits peuvent différerer d'une aude sur l'autre en fonction
        // du rôle)
        const userUiPermissions = [];
        if (context.user) {
          if (userHasPermission(context.user, "clone_aide")) {
            userUiPermissions.push("clone_aide");
          }
          if (
            userHasPermission(context.user, "edit_any_aide") ||
            userHasPermission(context.user, "edit_own_aide", { aide })
          ) {
            userUiPermissions.push("edit_aide");
          }
          if (
            userHasPermission(context.user, "delete_any_aide") ||
            userHasPermission(context.user, "delete_own_aide", { aide })
          ) {
            userUiPermissions.push("delete_aide");
          }
        }
        return {
          meta: {
            userUiPermissions
          },
          node: aide
        };
      });
      return {
        edges
      };
    }
  }
};
