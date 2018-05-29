const types = require("../types");
const AideModel = require("../../mongoose/Aide");
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
  GraphQLEnumType,
  GraphQLNonNull
} = require("graphql");
const { searchAides, getAides, getAide } = require("../../services/aide");

module.exports = {
  getAide: {
    type: types.Aide,
    args: {
      id: {
        type: GraphQLID
      }
    },
    resolve: async (_, { id }, context) => {
      return await getAide(id);
    }
  },
  /**
   * La query utilisée pour retournée les aides du moteur de recherche,
   * groupées par localisations
   */
  searchAides: {
    type: new GraphQLObjectType({
      name: "searchAidesResults",
      fields: () => {
        return {
          totalCount: { type: GraphQLInt },
          resultsGroups: {
            type: new GraphQLList(
              new GraphQLObjectType({
                name: "searchAideResultsGroup",
                fields: {
                  count: { type: GraphQLInt },
                  type: { type: GraphQLString },
                  label: { type: GraphQLString },
                  aides: { type: new GraphQLList(types.Aide) }
                }
              })
            )
          }
        };
      }
    }),
    args: {
      filters: {
        type: new GraphQLInputObjectType({
          name: "searchAidesFilters",
          fields: {
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
            perimetreApplicationType: {
              type: GraphQLNonNull(
                formatEnumForGraphQL(
                  "searchAidesPerimetreApplicationType",
                  enums.perimetreApplicationType
                )
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
              type: GraphQLString
            },
            demandeTiersPossible: {
              type: GraphQLBoolean
            }
          }
        })
      }
    },
    resolve: async (_, { filters = {}, sort }, context) => {
      return searchAides(filters, sort);
    }
  },
  allAides: {
    type: new GraphQLList(types.Aide),
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
            }
          }
        })
      }
    },
    resolve: async (_, { filters, sort = "-updatedAt" }, context) => {
      return getAides(filters, sort);
    }
  }
};
