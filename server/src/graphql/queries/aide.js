const types = require("../types");
const enums = require("../../enums/aide");
const { formatEnumForGraphQL } = require("../../services/enums");
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
      name: "getAideNode",
      fields: {
        node: { type: types.Aide }
      }
    }),
    args: {
      id: {
        type: GraphQLID
      }
    },
    resolve: async (_, { id }) => {
      return await { node: getAide(id) };
    }
  },
  /**
   * La query utilisée pour retournée les aides du moteur de recherche,
   * groupées par localisations
   */
  rechercheAides: {
    type: new GraphQLObjectType({
      name: "searchAidesResults",
      fields: () => {
        return {
          totalNombreAides: { type: GraphQLInt },
          groupesDeResultats: {
            type: new GraphQLList(searchAideResultsGroupType)
          }
        };
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
              type: formatEnumForGraphQL("searchAidesEtape", enums.etape)
            },
            statusPublication: {
              type: formatEnumForGraphQL(
                "searchAidesStatusPublication",
                enums.statusPublication
              )
            },
            type: {
              type: formatEnumForGraphQL("searchAidesType", enums.type)
            },
            // texte entré pour la recherche libre (par mots clefs)
            texte: {
              type: GraphQLString
            },
            // le perimetre initial de recherche: ex: département
            typePerimetreInitialDeRecherche: {
              type: formatEnumForGraphQL(
                "searchAidesTypePerimetreInitialDeRecherche",
                enums.perimetreApplicationType,
                false
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
              type: formatEnumForGraphQL(
                "searchAidesPerimetreApplicationType",
                enums.perimetreApplicationType
              )
            },
            destination: {
              type: formatEnumForGraphQL(
                "searchAidesDestination",
                enums.destination
              )
            },
            destinationAutre: {
              type: GraphQLString
            },
            formeDeDiffusionAutre: {
              type: GraphQLString
            },
            beneficiaires: {
              type: formatEnumForGraphQL(
                "searchAidesBeneficiaires",
                enums.beneficiaires
              )
            },
            perimetreApplicationCode: {
              type: GraphQLString
            },
            formeDeDiffusion: {
              type: formatEnumForGraphQL(
                "searchAidesFormeDeDiffusion",
                enums.formeDeDiffusion
              )
            },
            thematiques: {
              type: formatEnumForGraphQL(
                "searchAidesThematiques",
                enums.thematiques
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
    //type: new GraphQLList(types.Aide),
    type: new GraphQLObjectType({
      name: "allAides",
      fields: {
        edges: {
          type: new GraphQLList(
            new GraphQLObjectType({
              name: "allAideEdges",
              fields: {
                userNodePermissions: {
                  type: new GraphQLList(GraphQLString)
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
            auteur: { type: GraphQLString },
            etape: {
              type: formatEnumForGraphQL("allAidesEtape", enums.etape)
            },
            statusPublication: {
              type: formatEnumForGraphQL(
                "allAidesStatusPublication",
                enums.statusPublication
              )
            },
            type: {
              type: formatEnumForGraphQL("allAidesType", enums.type)
            },
            perimetreApplicationType: {
              type: formatEnumForGraphQL(
                "allAidesPerimetreApplicationType",
                enums.perimetreApplicationType
              )
            },
            destination: {
              type: formatEnumForGraphQL(
                "allAidesDestination",
                enums.destination
              )
            },
            destinationAutre: {
              type: GraphQLString
            },
            formeDeDiffusionAutre: {
              type: GraphQLString
            },
            beneficiaires: {
              type: formatEnumForGraphQL(
                "allAidesBeneficiaires",
                enums.beneficiaires
              )
            },
            perimetreApplicationCode: {
              type: GraphQLString
            },
            formeDeDiffusion: {
              type: formatEnumForGraphQL(
                "allAidesFormeDeDiffusion",
                enums.formeDeDiffusion
              )
            },
            thematiques: {
              type: formatEnumForGraphQL(
                "allAidesThematiques",
                enums.thematiques
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
        const userPermissions = [];
        if (
          userHasPermission(context.user, "edit_any_aide") ||
          userHasPermission(context.user, "edit_own_aide", { aide })
        ) {
          userPermissions.push("edit");
        }
        if (
          userHasPermission(context.user, "delete_any_aide") ||
          userHasPermission(context.user, "delete_own_aide", { aide })
        ) {
          userPermissions.push("delete");
        }
        return {
          userNodePermissions: userPermissions,
          node: aide
        };
      });
      return {
        edges
      };
    }
  }
};
