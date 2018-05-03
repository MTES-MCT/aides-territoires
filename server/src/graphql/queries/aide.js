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
              type: formatEnumForGraphQL("type", enums.type)
            },
            perimetreApplicationType: {
              type: formatEnumForGraphQL(
                "allAidesPerimetreApplicationType",
                enums.perimetreApplicationType
              )
            },
            perimetreApplicationCode: {
              type: GraphQLString
            },
            formeDeDiffusion: {
              type: GraphQLString
            }
          }
        })
      }
    },
    resolve: (_, { filters, sort = "-updatedAt" }, context) => {
      const query = AideModel.find(filters);
      query.sort(sort);
      return query;
    }
  }
};
