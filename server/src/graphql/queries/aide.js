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
