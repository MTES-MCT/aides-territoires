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
  GraphQLEnumType
} = require("graphql");

module.exports = {
  getAide: {
    type: types.Aide,
    args: {
      id: {
        type: GraphQLID
      }
    },
    resolve: async (_, { id }, context) => {
      return await AideModel.findById(id);
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
          count: { type: GraphQLInt },
          results: {
            type: new GraphQLList(
              new GraphQLObjectType({
                name: "searchAideResultsGroup",
                fields: {
                  count: { type: GraphQLInt },
                  type: { type: GraphQLString },
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
              type: GraphQLString
            },
            demandeTiersPossible: {
              type: GraphQLBoolean
            }
          }
        })
      }
    },
    resolve: async (_, {}, context) => {
      return {
        count: 15,
        results: [
          {
            count: 12,
            type: "departement",
            aides: [
              {
                nom: "aide numéro 1"
              },
              {
                nom: "aide numéro 2"
              }
            ]
          },
          {
            type: "motClefs",
            count: 3,
            aides: [
              {
                nom: "aide numéro 3"
              },
              {
                nom: "aide numéro 4"
              }
            ]
          }
        ]
      };
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
      // convert all array to mongosse $in syntax
      // example : {etape:{$in:["operationnel", "pre_operationnel", "fonctionnement"]}}
      for (filter in filters) {
        if (Array.isArray(filters[filter])) {
          filters[filter] = { $in: filters[filter] };
        }
      }
      const query = AideModel.find(filters);
      query.sort(sort);
      return query;
    }
  }
};
