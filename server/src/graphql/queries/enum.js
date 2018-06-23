const { GraphQLString, GraphQLObjectType, GraphQLList } = require("graphql");
const { getAllEnums } = require("../../services/enums");
const types = require("../types");

module.exports = {
  allEnums: {
    type: new GraphQLObjectType({
      name: "allEnums",
      fields: {
        edges: {
          type: new GraphQLList(
            new GraphQLObjectType({
              name: "allEnumsEdges",
              fields: {
                userNodePermissions: { type: GraphQLList(GraphQLString) },
                node: { type: types.Enum }
              }
            })
          )
        }
      }
    }),
    resolve: (_, args, context) => {
      const results = {};
      results.edges = getAllEnums().map(enumeration => {
        return {
          userNodePermissions: [],
          node: {
            ...enumeration
          }
        };
      });
      return results;
    }
  }
};
