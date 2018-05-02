const types = require("../types");
const AideModel = require("../../mongoose/Aide");
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
const { enums, formatEnumForGraphQL } = require("../../enums");
const aideEtapes = formatEnumForGraphQL("searchAideEtapes", enums.AIDE_ETAPES);
const aideStatusPublication = formatEnumForGraphQL(
  "searchAideStatusPublication",
  enums.AIDE_STATUS_PUBLICATION
);
const aideTypes = formatEnumForGraphQL("searchAideTypes", enums.AIDE_TYPES);
const aidePerimetreApplicationTypes = formatEnumForGraphQL(
  "searchAidePerimetreApplicationType",
  enums.AIDE_PERIMETRE_APPLICATION_TYPES
);

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
              type: new GraphQLList(aideEtapes)
            },
            statusPublication: {
              type: new GraphQLList(aideStatusPublication)
            },
            type: {
              type: new GraphQLList(aideTypes)
            },
            perimetreApplicationType: {
              type: new GraphQLList(aidePerimetreApplicationTypes)
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
